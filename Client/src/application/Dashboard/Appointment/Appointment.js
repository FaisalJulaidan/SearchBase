import React from 'react';

import { Icon, Typography, Tabs } from 'antd';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel';
import Calendar from './Calendar/Calendar';
import TimeSlots from './TimeSlots/TimeSlots';
import Appointments from './Appointments/Appointments';
import styles from './Calendar/Calendar.module.less';
import queryString from 'query-string';

import Availability from './Availability/Availability';

const { Title, Paragraph } = Typography;

class Appointment extends React.Component {

    state = {
        key: null,
        defaultTab: 'Conversations'
    };

    componentWillMount() {
        // Set tab from url search params
        let params = queryString.parse(this.props.location.search);
        if (['Appointments', 'Calendar', 'TimeSlots', 'Availability'].includes(params['tab']))
            this.setState({ defaultTab: params['tab'] });
    }


    render() {
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
                        <Appointments/>
                    </Tabs.TabPane>
                    <Tabs.TabPane disabled={true} tab="Calendar (coming soon)" key="Calendar">
                        <Calendar/>
                    </Tabs.TabPane>
                    <Tabs.TabPane tab="Time Slots" key="TimeSlots">
                        <TimeSlots openTab={this.state.key !== 'TimeSlots'}/>
                    </Tabs.TabPane>
                    <Tabs.TabPane tab="Availability" key="Availability">
                        <Availability/>
                    </Tabs.TabPane>
                </Tabs>
            </NoHeaderPanel>
        );
    }
}

export default Appointment;