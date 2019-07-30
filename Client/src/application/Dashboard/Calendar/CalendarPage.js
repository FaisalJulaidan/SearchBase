import React from 'react';
import {Tabs} from 'antd';
// import './Calendar.less'

import Calendar from './Calendar/Calendar'
import TimeSlots from './TimeSlots/TimeSlots'

class CalendarPage extends React.Component {
    render(){
        return (
            <Tabs>
                <Tabs.TabPane tab="Calendar" key="1">
                    <Calendar />
                </Tabs.TabPane>
                <Tabs.TabPane tab="Time Slots" key="1">
                    <TimeSlots />
                </Tabs.TabPane>
            </Tabs>
        )
    }
}

export default CalendarPage