import React from 'react'
import publicPage from '../../../hoc/PublicPage'
import {appointmentsPickerActions} from "store/actions";
import {Row, Col, Button, Typography, Modal} from 'antd'
import { history} from '../../../helpers'
import axios from 'axios'

const {Title} = Typography;
const {confirm} = Modal;

class AppointmentStatus extends React.Component {

    constructor(props){
        super(props)
        this.state = {
            pending: null
        }
    }

    setAppointmentStatus = (appointmentID, status) => {
        confirm({
            title: `Set appointment status to ${status}?`,
            content: `If you click OK, you will not be able to update the status of this appointment`,
            okType: 'danger',
            onOk: () => {
                console.log(this.props.token)
                axios.post("/api/appointments/set_status_public", {token: this.props.token, appointmentID: appointmentID, status: status},
                    {
                        headers: {'Content-Type': 'application/json'},
                    })


            },
            maskClosable: true
        });
    }
    render() {
        let name, appointment
        if(this.props.success){
            appointment = this.props.data.data
            name = appointment.Data.keywordsByDataType.Email[0]
        }
        return (
            <div>
                <h1>Setting appointment status</h1>
                {this.props.success ?
                    <div>
                        <Title level={4}>Appointment for {name}</Title>
                        <Row>
                            <Col span={24}>
                                <p>
                                    <b>Date & Time: </b>
                                    <span style={{color: '#9254de'}}>{appointment.DateTime}</span>
                                </p>
                            </Col>
                            <Col span={24}>
                                <p>
                                    <b>Appointment Status: </b>
                                    <span>
                                        <Button type="primary" icon="check" onClick={() => {this.setAppointmentStatus(appointment.ID, 'Accepted')}}>Accept</Button>
                                        <Button type="primary" icon="close" onClick={() => {this.setAppointmentStatus(appointment.ID, 'Rejected')}}>Reject</Button>
                                    </span>
                                </p>
                            </Col>
                        </Row>
                    </div>
                    :
                    <p>{this.props.error}</p>
                }

            </div>
        )

    }
}


export default publicPage(AppointmentStatus, 'token', '/', 'appointments/verify');
