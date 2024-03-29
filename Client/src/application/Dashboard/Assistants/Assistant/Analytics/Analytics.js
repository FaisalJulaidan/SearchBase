import React from 'react';
import styles from "./Analytics.module.less";

import Panel from 'components/Panel/Panel'
import {Chart, Axis, Tooltip, Geom } from "bizcharts";
import {analyticsActions} from "store/actions";
import {connect} from 'react-redux';
import {Icon, Spin, Button, Row, Col, Statistic} from 'antd';
import moment from 'moment';


const splits = {
        yearly: {format:"YYYY", render: 'MMM', compare: "month"},
        monthly: {format:"MMM", render:"D", compare: "days"},
        daily: {format: "ddd", render: "HH", compare: "hour"}};
const visitData = [];
const beginDay = new Date().getTime();

for (let i = 0; i < 10; i += 1) {
    visitData.push({
        x: moment(new Date(beginDay + (1000 * 60 * 60 * 24 * i))).format('MMM-DD'),
        y: Math.floor(Math.random() * 100) + 10,
        z: '123'
    });
}

class Analytics extends React.Component {
    //split can  be yearly/monthly/daily/hourly
    constructor(props){
        super(props);
        this.state = {
            height: 100,
            split: "yearly",
            curDate: moment()
        };
        this.changeSplit = this.changeSplit.bind(this);
        this.iterator = this.iterator.bind(this)
    }

    chartDiv;

    componentDidMount() {
        const height = this.chartDiv.clientHeight;
        this.setState({height});
    }
    componentWillMount(){
        const {assistant} = this.props;
        this.props.dispatch(analyticsActions.fetchAnalytics(assistant.ID))
    }

    changeSplit(split){
        const {analytics} = this.props;
        if(split !== this.state.split){
            this.setState({split})
        }
    }

    dateFormatting(split) {
        switch(split){
            case "yearly":
                return new Array(12).fill(1).map((i, x) => {return moment(this.state.curDate).set('month', x)});
            case "monthly":
                return new Array(moment(this.state.curDate).daysInMonth()).fill(1).map((i, x) => {return moment(this.state.curDate).set('date', x+1 )});
            case "daily":
                return new Array(24).fill(1).map((i, x) => {return moment(this.state.curDate).set('hour', x)})
        }
    }

    iterator(change){
        switch(this.state.split){
            case "yearly":
                this.setState({curDate: this.state.curDate.set('year', this.state.curDate.get('year')+change)});
                break;
            case "monthly":
                this.setState({curDate: this.state.curDate.set('month', this.state.curDate.get('month')+change)});
                break;
            case "daily":
                this.setState(({curDate: this.state.curDate.set('day', this.state.curDate.get('day') + change)}));
                break;
        }
    }

    timeSpentChatting() {
        const {analytics} = this.props.analytics;
        let compareTo = moment();
        // Filters the analytics array so that it gets only the current time (year/month etc) then accumulates all the
        // total timespent values, and divides by the length of the array to get the average, also rounds to 2 digits

        let timeSpent = ["year", "month", "day"];
        let current = timeSpent.map(t =>
            analytics.filter(a => moment(a.DateTime).isSame(compareTo, t))
                .reduce((a, n, i, ba) => (a + parseInt(n.TimeSpent)) / (ba.length - 1 === i ? ba.length : 1), 0)
                .toFixed(2));
        let previous = timeSpent.map(t =>
            analytics.filter(a => moment(a.DateTime).isSame(compareTo.clone().subtract(1, t), t))
                .reduce((a, n, i, ba) => (a + parseInt(n.TimeSpent)) / (ba.length - 1 === i ? ba.length : 1), 0)
                .toFixed(2));

        return {current, previous}
    }

    userApplications(){
        const {analytics} = this.props.analytics;
        return {accepted: analytics.filter(a=> a.ApplicationStatus==="Accepted").length,
                pending: analytics.filter(a=> a.ApplicationStatus==="Pending").length,
                rejected: analytics.filter(a=> a.ApplicationStatus==="Rejected").length,}
    }

    averageScore(){
        const {analytics} = this.props.analytics;
        return (analytics.reduce((a, i) => a + parseInt(i.Score), 0) / analytics.length ).toFixed(2)
    }

    candidateClientSplit(){
        const {analytics} = this.props.analytics;
        return {clients: analytics.filter(a=> a.UserType==="Client").length,
            candidates: analytics.filter(a=> a.UserType==="Candidate").length}
    }


    render() {
        const {analytics} = this.props.analytics;
        const {split} = this.state;
        let data, tsc, userApplications, averageScore, clientCandidate; // timeSpentChatting = tsc

        if(!this.props.analytics.isLoading && analytics){
            data = this.dateFormatting(split).map(t =>
                ({time: t.format(splits[this.state.split].render), chats: analytics.filter(a => moment(a.DateTime).isSame(t, splits[split].compare)).length}))
            tsc = this.timeSpentChatting();
            userApplications = this.userApplications();
            averageScore = this.averageScore();
            clientCandidate = this.candidateClientSplit();
            // maybe move timeSpent to onload to save resources , no need to constantly recalculate? idk
        }

        console.log("==========");
        console.log(data);
        const cols = {
            chats: {
                min: 0
            },
            time: {
                range: [0, 1]
            }
        };
        return (
            <>
                <Row gutter={16}>
                    <Col span={18}>
                        <Panel>
                            {/* Panel Header*/}
                            <div>
                                <h3>
                                    <Icon type="fund" theme="twoTone" twoToneColor={"#9254de"}/> Chats
                                </h3>
                            </div>

                            {/* Panel Body*/}
                            <div align="center" ref={chartDiv => this.chartDiv = chartDiv}>
                                {!data ?
                                    <Spin/> :
                                    <>
                                        <Button style={{marginRight: 8}} onClick={() => this.changeSplit('yearly')} type={split==="yearly" ? "primary" : null}>Yearly</Button>
                                        <Button style={{marginRight: 8}} onClick={() => this.changeSplit('monthly')} type={split==="monthly" ? "primary" : null}>Monthly</Button>
                                        <Button onClick={() => this.changeSplit('daily')} type={split==="daily" ? "primary" : null}>Daily</Button>

                                        <div className={styles.Date_Selector}>
                                            <Icon type="caret-left" onClick={() => {this.iterator(-1)}} />
                                            <h1>{moment(this.state.curDate).format(splits[this.state.split].format)}</h1>
                                            <Icon type="caret-right" onClick={() => {this.iterator(1)}}/>
                                        </div>

                                        <Chart height={500} data={data} scale={cols} forceFit>
                                            <Axis name="time    " />
                                            <Axis name="chats" />
                                            <Tooltip
                                                crosshairs={{
                                                    type: "y"
                                                }}
                                            />
                                            <Geom type="line" position="time*chats" size={2} />
                                            <Geom
                                                type="point"
                                                position="time*chats"
                                                size={4}
                                                shape={"square"}
                                                style={{
                                                    stroke: "#fff",
                                                    lineWidth: 1
                                                }}
                                            />
                                        </Chart>
                                    </>
                                }
                            </div>

                        </Panel>
                    </Col>

                    <Col span={6}>
                        <Panel>
                            {/* Panel Header*/}
                            <div>
                                <h3>
                                    <Icon type="team" style={{color: "#9254de"}}/> User Applications
                                </h3>
                            </div>

                            {/* Panel Body*/}
                            <div align="center">
                                {!userApplications ?
                                    <Spin/> :
                                    <Row gutter={16}>
                                        <Col span={8}>
                                            <Statistic title="Accepted" value={userApplications.accepted}
                                                       prefix={<Icon type="check-circle" theme="twoTone"
                                                                     twoToneColor="#2ecc71"/>}/>
                                        </Col>
                                        <Col span={8}>
                                            <Statistic title="Pending" value={userApplications.pending}
                                                       prefix={<Icon type="minus-circle" theme="twoTone"
                                                                     twoToneColor="#f1c40f"/>}/>
                                        </Col>
                                        <Col span={8}>
                                            <Statistic title="Rejected" value={userApplications.rejected}
                                                       prefix={<Icon type="close-circle" theme="twoTone"
                                                                     twoToneColor="#e74c3c"/>}/>
                                        </Col>
                                    </Row>
                                }
                            </div>

                        </Panel>

                        <Panel>
                            {/* Panel Header*/}
                            <div>
                                <h3>
                                    <Icon type="eye" theme="twoTone" twoToneColor="#9254de"/> Time spent chatting
                                </h3>
                            </div>

                            {/* Panel Body*/}
                            <div align="center">
                                {!tsc ?
                                    <Spin /> :
                                    <Row gutter={16}>
                                        <Col span={8}>
                                            <Statistic title="Yearly average"
                                                       value={(Math.floor(tsc.current[0]/60)) + "m" }
                                                       suffix={Math.floor(tsc.current[0] % 60) + "s"}
                                                       prefix={<Icon type={tsc.current[0] > tsc.previous[0] ? "caret-up" : "caret-down"} />} />
                                        </Col>
                                        <Col span={8}>
                                            <Statistic title="Monthly average"
                                                       value={(Math.floor(tsc.current[1]/60)) + "m" }
                                                       suffix={Math.floor(tsc.current[1] % 60) + "s"}
                                                       prefix={<Icon type={tsc.current[1] > tsc.previous[1] ? "caret-up" : "caret-down"} />} />
                                        </Col>
                                        <Col span={8}>
                                            <Statistic title="Daily average"
                                                       value={(Math.floor(tsc.current[2]/60)) + "m" }
                                                       suffix={Math.floor(tsc.current[2] % 60) + "s"}
                                                       prefix={<Icon type={tsc.current[2] > tsc.previous[2] ? "caret-up" : "caret-down"} />} />
                                        </Col>
                                    </Row>
                                }
                            </div>

                        </Panel>

                        <Panel>
                            {/* Panel Header*/}
                            <div>
                                <h3>
                                    <Icon type="team" style={{color: "#9254de"}}/> Average Score
                                </h3>
                            </div>

                            {/* Panel Body*/}
                            <div align="center">
                                {!averageScore ?
                                    <Spin/> :
                                    <Row>
                                        <Col>
                                            <Statistic value={averageScore}/>
                                        </Col>
                                    </Row>
                                }
                            </div>

                        </Panel>

                        <Panel>
                            {/* Panel Header*/}
                            <div>
                                <h3>
                                    <Icon type="team" style={{color: "#9254de"}}/> Clients Candidate split
                                </h3>
                            </div>

                            {/* Panel Body*/}
                            <div align="center">
                                {!clientCandidate ?
                                    <Spin/> :
                                    <Row >
                                        <Col span={12}>
                                            <Statistic title="Clients" value={clientCandidate.clients}/>
                                        </Col>
                                        <Col span={12}>
                                            <Statistic title="Candidates" value={clientCandidate.candidates}/>
                                        </Col>
                                    </Row>

                                }
                            </div>
                        </Panel>
                    </Col>

                </Row>

            </>

        );
    }
}

const mapStateToProps = state =>  {
    return {
        analytics: state.analytics,
    };
};

export default connect(mapStateToProps)(Analytics);

