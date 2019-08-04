import React from 'react';

import {Icon, Input, Modal,Typography, Tabs} from 'antd';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import Calendar from './Calendar/Calendar'
import TimeSlots from './TimeSlots/TimeSlots'
import Appointments from './Appointments/Appointments'
import styles from "./Calendar/Calendar.module.less";
import {history} from "../../../helpers";
import {Switch, Route} from 'react-router-dom'


const {Title, Paragraph} = Typography;
const { TextArea } = Input;
const { confirm } = Modal;

const tabs = {"1": "", "2" : "calendar", "3": "timeslots"}

class Appointment extends React.Component {
    state = {
        key: null
    }


    render(){
        const key = this.state.key ? this.state.key : this.props.defaultTab ? this.props.defaultTab : "1"
        return (
            <NoHeaderPanel>
                <div className={styles.Header}>
                    <Title className={styles.Title}>
                        <Icon type="calendar"/> Appointments
                    </Title>
                    <Paragraph type="secondary">
                        Here you can find all data relating to your appointments
                    </Paragraph>
                </div>
                <Tabs onChange={key =>  this.setState({key: key})} activeKey={key}>
                    <Tabs.TabPane tab="Appointments" key="1">
                        <Appointments/>
                    </Tabs.TabPane>
                    <Tabs.TabPane tab="Calendar" key="2">
                        <Calendar />
                    </Tabs.TabPane>
                    <Tabs.TabPane tab="Time Slots" key="3">
                        <TimeSlots openTab={this.state.key === "2" ? true : false}/>
                    </Tabs.TabPane>
                </Tabs>
            </NoHeaderPanel>
        )
    }
}

export default Appointment