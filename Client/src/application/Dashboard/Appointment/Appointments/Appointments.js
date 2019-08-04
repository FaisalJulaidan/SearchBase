import React from 'react';

import {Table, Button, Spin, Icon} from 'antd'
import {appointmentActions} from "store/actions";

import LoadingSpinner from "components/LoadingSpinner/LoadingSpinner";

import styles from './Appointments.module.less'

import { connect } from 'react-redux'

const antIcon = <Icon type="loading" style={{ fontSize: 24 }} spin />

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


    refresh = () => {
        this.props.dispatch(appointmentActions.fetchAppointments())
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
            render: item => item.isLoading ? <Spin indicator={antIcon} /> : item.Status === "Pending" ?  <Button onClick={() => this.approve(item.ID)}>Approve</Button> : "Status has already been set"
        },
        {
            title: 'Reject',
            dataIndex: 'reject',
            key: 'reject',
            render: item =>  item.isLoading ? <Spin indicator={antIcon} />  : item.Status === "Pending" ?  <Button onClick={() => this.reject(item.ID)}>Reject</Button> : "Status has already been set"
        },
    ]
    render() {
        const realList = this.props.appointments.map(item => ({ email : item.Conversation.keywordsByDataType.Email[0],
                                                                         status: item.Status,
                                                                         approve: item,
                                                                         reject: item}))
        return (<>
                    <h1>Appointment list
                        <div className={styles.refresh_button}>
                            <Button type="primary" icon="sync" disabled={this.props.isLoading}
                                                    onClick={this.refresh}>
                                Refresh
                            </Button>
                        </div>
                    </h1>
                    {this.props.isLoading ? <LoadingSpinner /> :<Table dataSource={realList} columns={this.columns}/>}
                </>)
    }
}
function mapStateToProps(state) {
    console.log(state.appointment.isLoading)
    return {
        appointments: state.appointment.appointments,
        isLoading: state.appointment.isLoading
    };
}

export default connect(mapStateToProps, null)(Appointments)