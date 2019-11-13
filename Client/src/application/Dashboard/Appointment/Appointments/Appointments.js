import React from 'react';

import { Table, Button, Spin, Icon, Modal, Popconfirm } from 'antd';
import { appointmentActions } from 'store/actions';
import { convertTimezone } from 'helpers';


import styles from './Appointments.module.less';

import { connect } from 'react-redux';

const confirm = Modal.confirm;

const antIcon = <Icon type="loading" style={{ fontSize: 24 }} spin/>;

class Appointments extends React.Component {

    componentDidMount() {
        this.props.dispatch(appointmentActions.fetchAppointments());
    }

    approve = (id, name, email, phone) => {
        confirm({
            title: `Accept appointment confirmation`,
            content: `If you click Approve, this user will receive a confirmation email about this appointment and you cannot undo that`,
            onOk: () => {this.props.dispatch(appointmentActions.setAppointmentStatusRequest(id, 'Accepted'))},
            okText: "Approve",
        });

    };

    reject = (id, name, email, phone) => {
        confirm({
            title: `Reject appointment confirmation`,
            content: `If you click Reject, this appointment will be deleted forever and you cannot undo that but it will make the appointment time slot available again for other new candidates to pick`,
            onOk: () => {this.props.dispatch(appointmentActions.setAppointmentStatusRequest(id, 'Rejected'))},
            okText: "Reject",
        });
    };


    refresh = () => {
        this.props.dispatch(appointmentActions.fetchAppointments());
    };


    columns = [
        {
            title: 'Email',
            dataIndex: 'email',
            key: 'email'
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status'
        },
        {
            title: 'Time',
            dataIndex: 'time',
            key: 'time'
        },
        {
            title: 'Approve',
            dataIndex: 'approve',
            key: 'approve',
            render: item => item.isLoading ? <Spin indicator={antIcon}/> : item.Status === 'Pending' ?
                <Button onClick={() => this.approve(item.ID, item.Conversation.Name, item.Conversation.Email, item.Conversation.PhoneNumber)}>Approve</Button> : 'Status has already been set'
        },
        {
            title: 'Reject',
            dataIndex: 'reject',
            key: 'reject',
            okType: 'danger',
            render: item => item.isLoading ? <Spin indicator={antIcon}/> : item.Status === 'Pending' ?
                <Button onClick={() => this.reject(item.ID, item.Conversation.Name, item.Conversation.Email, item.Conversation.PhoneNumber)}>Reject</Button> : 'Status has already been set'
        }
    ];

    render() {
        const realList = this.props.appointments.map(item => ({
            key: item.ID,
            time: convertTimezone(item.DateTime, 'ddd, DD MMM YYYY h:mm a'),
            email: item.Conversation.Email,
            status: item.Status,
            approve: item,
            reject: item
        }));
        return (<>
            <h1>Appointment list
                <div className={styles.refresh_button}>
                    <Button type="primary" icon="sync" disabled={this.props.isLoading}
                            onClick={this.refresh}>
                        Refresh
                    </Button>
                </div>
            </h1>
            <Table dataSource={realList} loading={this.props.isLoading} columns={this.columns}/>
        </>);
    }
}

function mapStateToProps(state) {
    return {
        appointments: state.appointment.appointments,
        isLoading: state.appointment.isLoading
    };
}

export default connect(mapStateToProps, null)(Appointments);