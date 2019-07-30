import React from 'react';

import {Icon, Input, Modal,Typography, Tabs} from 'antd';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import Calendar from './Calendar/Calendar'
import TimeSlots from './TimeSlots/TimeSlots'
import styles from "./Calendar/Calendar.module.less";


const {Title, Paragraph} = Typography;
const { TextArea } = Input;
const { confirm } = Modal;

class CalendarPage extends React.Component {
    render(){
        return (
            <NoHeaderPanel>
                <div className={styles.Header}>
                    <Title className={styles.Title}>
                        <Icon type="calendar"/> Calendar
                    </Title>
                    <Paragraph type="secondary">
                        Here you can find all assigned calendars
                    </Paragraph>
                </div>
                <Tabs>
                <Tabs.TabPane tab="Calendar" key="1">
                    <Calendar />
                </Tabs.TabPane>
                <Tabs.TabPane tab="Time Slots" key="2">
                    <TimeSlots />
                </Tabs.TabPane>
            </Tabs>
            </NoHeaderPanel>
        )
    }
}

export default CalendarPage