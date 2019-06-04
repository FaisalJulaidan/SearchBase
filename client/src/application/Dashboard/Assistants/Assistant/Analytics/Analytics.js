import React from 'react';
import styles from "./Analytics.module.less";

import Header from "../../../../../components/Header/Header";
import {Chart, Axis, Tooltip, Geom } from "bizcharts";
import {analyticsActions} from "store/actions";
import {connect} from 'react-redux';
import NumberInfo from 'ant-design-pro/lib/NumberInfo';
import {Icon, Spin, Button} from 'antd';

import moment from 'moment';

const splits = {
        yearly: {format:"YYYY", render: 'MMM', compare: "month"},
        monthly: {format:"MMM", render:"D", compare: "days"},
        daily: {format: "ddd", render: "HH", compare: "hour"}}

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
        super(props)
        this.state = {
            height: 100,
            split: "yearly",
            curDate: moment()
        };
        this.changeSplit = this.changeSplit.bind(this)
        this.iterator = this.iterator.bind(this)
    }

    chartDiv;

    componentDidMount() {
        const height = this.chartDiv.clientHeight;
        this.setState({height});
    }
    componentWillMount(){
        const {assistant} = this.props.location.state;
        this.props.dispatch(analyticsActions.fetchAnalytics(assistant.ID))
    }
    changeSplit(split){
        const {analytics} = this.props.analytics
        if(split !== this.state.split){
            this.setState({split})
        }
    }

    dateFormatting(split) {
        switch(split){
            case "yearly":
                return new Array(12).fill(1).map((i, x) => {return moment(this.state.curDate).set('month', x)});
                break;
            case "monthly":
                return new Array(moment(this.state.curDate).daysInMonth()).fill(1).map((i, x) => {return moment(this.state.curDate).set('date', x+1 )});
                break;
            case "daily":
                return new Array(24).fill(1).map((i, x) => {return moment(this.state.curDate).set('hour', x)})
                break;
        }
    }
    iterator(change){
        switch(this.state.split){
            case "yearly":
                this.setState({curDate: this.state.curDate.set('year', this.state.curDate.get('year')+change)})
                break;
            case "monthly":
                this.setState({curDate: this.state.curDate.set('month', this.state.curDate.get('month')+change)})
                break;
            case "daily":
                this.setState(({curDate: this.state.curDate.set('day', this.state.curDate.get('day') + change)}))
                break;
        }
    }


    render() {
        const {analytics} = this.props.analytics
        const {split} = this.state;
        let data = this.props.analytics.isLoading
                    ? null
                    : this.dateFormatting(split).map(t =>
                        ({time: t.format(splits[this.state.split].render), chats: analytics.filter(a => moment(a.DateTime).isSame(t, splits[split].compare)).length}))
        const cols = {
            chats: {
                min: 0
            },
            time: {
                range: [0, 1]
            }
        };
        console.log(data)
        return (
            <div style={{height: '100%'}}>
                <div style={{padding: '0 5px'}}>
                    <div style={{width: '100%', height: 56, marginBottom: 10}}>
                        <Header display={"Analytics Page"}/>
                    </div>
                </div>

                <div style={{height: 'calc(100% - 66px)', width: '100%', display: 'flex'}}>
                    <div style={{margin: 5, width: '70%'}}>
                        <div className={styles.Panel}>
                                <div className={styles.Panel_Header}>
                                    <h3>
                                        <Icon type="fund" theme="twoTone" twoToneColor={"#9254de"}/> Chats
                                    </h3>
                                </div>

                                <div className={styles.Panel_Body}
                                     ref={chartDiv => this.chartDiv = chartDiv}>
                                    <Button onClick={() => this.changeSplit('yearly')} type={split==="yearly" ? "primary" : null}>Yearly</Button>
                                    <Button onClick={() => this.changeSplit('monthly')} type={split==="monthly" ? "primary" : null}>Monthly</Button>
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
                                </div>
                        </div>
                    </div>

                    <div style={{height: '100%', width: '30%', margin: 5}}>
                        <div style={{height: 'calc(50% - 5px)', marginBottom: 5}}>
                            <div className={styles.Panel}>
                                <Spin size="large" tip="Coming Soon">
                                    <div className={styles.Panel_Header}>
                                        <h3>
                                            <Icon type="team" style={{color: "#9254de"}}/> Total Users
                                        </h3>
                                    </div>

                                    <div className={styles.Panel_Body}>
                                        <NumberInfo
                                            subTitle={<span>All Users</span>}
                                            total={123.0}
                                            subtitle={<span>The total users number used this assistant</span>}
                                        />
                                    </div>
                                </Spin>
                            </div>
                        </div>

                        <div style={{height: 'calc(50% - 10px)'}}>
                            <div className={styles.Panel}>
                                <Spin size="large" tip="Coming Soon">
                                    <div className={styles.Panel_Header}>
                                        <h3>
                                            <Icon type="eye" theme="twoTone" twoToneColor="#9254de"/> Total Visits
                                        </h3>
                                    </div>

                                    <div className={styles.Panel_Body}>
                                        <NumberInfo
                                            subTitle={<span>Visits this week</span>}
                                            total={12321.0}
                                            status="up"
                                            subTotal={17.1}
                                        />
                                    </div>
                                </Spin>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        );
    }
}

const mapStateToProps = state =>  {
    return {
        analytics: state.analytics,
    };
};

export default connect(mapStateToProps)(Analytics);
// export default Analytics

