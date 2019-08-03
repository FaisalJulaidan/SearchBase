import React from 'react';

import {Table, Button} from 'antd'
import {appointmentActions} from "store/actions";

import Appointment from './Appointment'

import { connect } from 'react-redux'

class Appointments extends React.Component {

    componentDidMount() {
        this.props.dispatch(appointmentActions.fetchAppointments())
    }

    approve = (id) => {
        this.props.dispatch(appointmentActions.setAppointmentStatusRequest(id, 'Accepted'))
    }

    reject = (id) => {
        this.props.dispatch(appointmentActions.setAppointmentStatusRequest(id, 'Rejected'))
    }


    columns = [
        {
            title: 'Email',
            dataIndex: 'email',
            key: 'email',
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
        },
        {
            title: 'Approve',
            dataIndex: 'approve',
            key: 'approve',
            render: item => item.Status === "Pending" ?  <Button onClick={() => this.approve(item.ID)}>Approve</Button> : "Status has already been set"
        },
        {
            title: 'Reject',
            dataIndex: 'reject',
            key: 'reject',
            render: item => item.Status === "Pending" ?  <Button onClick={() => this.reject(item.ID)}>Reject</Button> : "Status has already been set"
        },
    ]
    render() {
        if(this.props.appointments.length === 0 ) { return null }
        const realList = this.props.appointments.map(item => ({ email : item.Conversation.keywordsByDataType.Email[0],
                                                                         status: item.Status,
                                                                         approve: item,
                                                                         reject: item}))
        return (<>
                    <h1>Appointment list</h1>
                    <Table dataSource={realList} columns={this.columns} />;
                </>)
    }
}
function mapStateToProps(state) {
    return {
        appointments: state.appointment.appointments,
    };
}

export default connect(mapStateToProps, null)(Appointments)