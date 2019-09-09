import React from 'react';

import { Icon, Input, Modal, Typography, Tabs } from 'antd';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel';
import Calendar from './Calendar/Calendar';
import TimeSlots from './TimeSlots/TimeSlots';
import momenttz from 'moment-timezone';
import Appointments from './Appointments/Appointments';
import styles from './Calendar/Calendar.module.less';
import queryString from 'query-string';
// import {TimezoneContext} from "../../../contexts/timezone"

import { TimezoneContext } from '../../../contexts/timezone';

const { Title, Paragraph } = Typography;

class Appointment extends React.Component {

    state = {
        key: null,
        defaultTab: 'Conversations'
    };

    componentWillMount() {
        // Set tab from url search params
        let params = queryString.parse(this.props.location.search);
        if (['Appointments', 'Calendar', 'TimeSlots'].includes(params['tab']))
            this.setState({ defaultTab: params['tab'] });
    }


    static contextType = TimezoneContext;

    render() {
        let tz = this.context ? this.context : momenttz.tz.guess();
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
                <Tabs onChange={key => this.setState({ key: key })} defaultActiveKey={this.state.defaultTab}>
                    <Tabs.TabPane tab="Appointments" key="Appointments">
                        <Appointments tz={tz}/>
                    </Tabs.TabPane>
                    <Tabs.TabPane tab="Calendar" key="Calendar">
                        <Calendar tz={tz}/>
                    </Tabs.TabPane>
                    <Tabs.TabPane tab="Time Slots" key="TimeSlots">
                        <TimeSlots openTab={this.state.key !== 'TimeSlots'} tz={tz}/>
                    </Tabs.TabPane>
                </Tabs>
            </NoHeaderPanel>
        );
    }
}

export default Appointment;