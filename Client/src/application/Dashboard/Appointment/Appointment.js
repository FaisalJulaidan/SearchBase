import React from 'react';

import {Icon, Input, Modal,Typography, Tabs} from 'antd';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import Calendar from './Calendar/Calendar'
import TimeSlots from './TimeSlots/TimeSlots'
import Appointments from './Appointments/Appointments'
import styles from "./Calendar/Calendar.module.less";


const {Title, Paragraph} = Typography;
const { TextArea } = Input;
const { confirm } = Modal;

class Appointment extends React.Component {
    render(){
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
                <Tabs>
                <Tabs.TabPane tab="Calendar" key="1">
                    <Calendar />
                </Tabs.TabPane>
                <Tabs.TabPane tab="Time Slots" key="2">
                    <TimeSlots/>
                </Tabs.TabPane>
                <Tabs.TabPane tab="Appointments" key="3">
                    <Appointments/>
                </Tabs.TabPane>
            </Tabs>
            </NoHeaderPanel>
        )
    }
}

export default Appointment