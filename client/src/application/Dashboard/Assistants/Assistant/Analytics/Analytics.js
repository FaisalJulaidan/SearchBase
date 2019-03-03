import React from 'react';
import styles from "./Analytics.module.less";

import Header from "../../../../../components/Header/Header";
import {Bar} from "ant-design-pro/lib/Charts";
import NumberInfo from 'ant-design-pro/lib/NumberInfo';
import {Icon} from 'antd';

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
    }

    render() {
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
                                <Bar
                                    color={"#9254de"}
                                    height={this.state.height - 30}
                                    title="Users Over Date"
                                    data={visitData}
                                />
                            </div>
                        </div>
                    </div>

                    <div style={{height: '100%', width: '30%', margin: 5}}>
                        <div style={{height: 'calc(50% - 5px)', marginBottom: 5}}>
                            <div className={styles.Panel}>
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
                            </div>
                        </div>

                        <div style={{height: 'calc(50% - 10px)'}}>
                            <div className={styles.Panel}>
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
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        );
    }
}

export default Analytics;