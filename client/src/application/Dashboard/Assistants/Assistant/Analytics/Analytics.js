import React from 'react';
import styles from "./Analytics.module.less";

import Header from "../../../../../components/Header/Header";
import {Chart, Axis, Tooltip, Geom } from "bizcharts";
import {analyticsActions} from "store/actions";
import {connect} from 'react-redux';
import NumberInfo from 'ant-design-pro/lib/NumberInfo';
import {Icon, Spin} from 'antd';

import moment from 'moment';

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
    state = {
        height: 100
    };
    chartDiv;

    componentDidMount() {
        const height = this.chartDiv.clientHeight;
        this.setState({height});
        console.log(this.props)
    }
    componentWillMount(){
        const {assistant} = this.props.location.state;
        this.props.dispatch(analyticsActions.fetchAnalytics(assistant.ID))
    }




    render() {
        const data = [
            {
                year: "1991",
                value: 3
            },
            {
                year: "1992",
                value: 4
            },
            {
                year: "1993",
                value: 3.5
            },
            {
                year: "1994",
                value: 5
            },
            {
                year: "1995",
                value: 4.9
            },
            {
                year: "1996",
                value: 6
            },
            {
                year: "1997",
                value: 7
            },
            {
                year: "1998",
                value: 9
            },
            {
                year: "1999",
                value: 13
            }
        ];
        const cols = {
            value: {
                min: 0
            },
            year: {
                range: [0, 1]
            }
        };
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
                                        <Icon type="fund" theme="twoTone" twoToneColor={"#9254de"}/> Monthly Records
                                    </h3>
                                </div>

                                <div className={styles.Panel_Body}
                                     ref={chartDiv => this.chartDiv = chartDiv}>
                                    <Chart height={500} data={data} scale={cols} forceFit>
                                        <Axis name="year" />
                                        <Axis name="value" />
                                        <Tooltip
                                            crosshairs={{
                                                type: "y"
                                            }}
                                        />
                                        <Geom type="line" position="year*value" size={2} />
                                        <Geom
                                            type="point"
                                            position="year*value"
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
    // const {analytics} = state;
    console.log(state)
    return {
        options: state.options.options,
    };
};

export default connect(mapStateToProps)(Analytics);
// export default Analytics

