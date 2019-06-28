import React from 'react';
import {connect} from 'react-redux';
import styles from './Calendar.module.less'
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Badge, Calendar as AntdCalendar, Col, Divider, Icon, Input, Modal, Row, Typography, List} from 'antd';
import moment from 'moment';
import {appointmentActions} from "store/actions";
import './Calendar.less'

const {Title, Paragraph} = Typography;
const { TextArea } = Input;
const { confirm } = Modal;

class Calendar extends React.Component {

    constructor(props){
        super(props)
        this.state = {
            value: moment(),
            appointmentModalVisible: false,
            appointments: []
        };
    }

    componentDidMount() {
        const {assistant} = this.props;
        this.props.dispatch(appointmentActions.fetchAppointments(assistant.ID))
    }

    onCloseModal = () => {
        this.setState({appointmentModalVisible: false});
    };

    onSelect = value => {
        let d = this.state.appointments.filter(d => value.utc().isSame(moment(d.DateTime).utc(), 'day'))

        if (d.length)
            this.setState({value, appointmentModalVisible: true});
    };

    onPanelChange = value => this.setState({value});


    dateCellRender = (value) => {
        let d = this.state.appointments.filter(d => value.utc().isSame(moment(d.DateTime).utc(), 'day')).filter(d => d.Status !== "Pending")
        let pending = this.state.appointments.filter(d => d.Status === "Pending")
        return (
            <ul className="events">
                {d.length !== 0 ?
                    <li>
                        <Badge status="warning" text={`${d.length} `+ (d.length === 1 ? 'Appointment' : 'Appointments' )}/>
                        { pending.length !== 0 ?
                            <Badge status="error" text={`${pending.length} ${(pending.length === 1 ? 'Appointment' : 'Appointments' )} pending approval `}/>
                        : null}
                    </li>
                : null}
            </ul>
        );
    };

    getMonthData = (value) => {
        if (value.month() === 8) {
            return 8;
        }
    };

    monthCellRender = (value) => {
        const num = this.getMonthData(value);
        return num ? (
            <div className="notes-month">
                <section>{num}</section>
                <span>Candidates</span>
            </div>
        ) : null;
    };

    setAppointmentStatus = (appointmentID, status) => {
        confirm({
            title: `Set appointment status to ${status}?`,
            content: `If you click OK, you will not be able to update the status of this appointment`,
            okType: 'danger',
            onOk: () => {
                this.props.dispatch(appointmentActions.setAppointmentStatusRequest(appointmentID, status))
                let {appointments} = this.state
                this.setState({
                    appointments: appointments.map(a => ({
                        ...a,
                        Status: a.ID === appointmentID ? status : a.Status
                    }))
                })
            },
            maskClosable: true
        });
    }

    componentWillReceiveProps(nextProps) {
        if(nextProps.appointments && this.state.appointments.length === 0){
            this.setState({appointments: nextProps.appointments})
        }
    }

    render() {
        const {value} = this.state;
        const visibleAppointments = this.state.appointments.filter(d => value.utc().isSame(moment(d.DateTime).utc(), 'day'))
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

                <div>
                    {this.props.appointments ?
                    <React.Fragment>
                        <AntdCalendar value={value} onSelect={this.onSelect} onPanelChange={this.onPanelChange}
                                      dateCellRender={this.dateCellRender} monthCellRender={this.monthCellRender}/>
                        <Modal title="Appointments Details"
                               width={640}
                               className={'custom_calendar'}
                               onCancel={this.onCloseModal}
                               onOk={this.onCloseModal}
                               okText="Save"
                               cancelText="Cancel"
                               visible={this.state.appointmentModalVisible}>
                            {
                                visibleAppointments.map((a, index) =>{
                                    let name = a.Conversation.keywordsByDataType.Email[0]
                                    return (
                                    <div key={index}>
                                        <Title level={4}>Appointment for {name}</Title>
                                        <Row>
                                            <Col span={24}>
                                                <p>
                                                    <b>Date & Time: </b>
                                                    <span style={{color: '#9254de'}}>{a.DateTime}</span>
                                                </p>
                                            </Col>
                                            <Col span={24}>
                                                <p>
                                                    <b>Appointment Status: </b>
                                                    {a.Status === "Pending" ?
                                                        <span>
                                                            <button onClick={() => {this.setAppointmentStatus(a.ID, 'Accepted')}}>Accept</button>
                                                            <button onClick={() => {this.setAppointmentStatus(a.ID, 'Rejected')}}>Reject</button>
                                                        </span>
                                                        :
                                                        <span>{a.Status}</span>
                                                    }
                                                </p>
                                            </Col>

                                            <Col span={24}>
                                                <p><b>Notes:</b></p>
                                                <TextArea
                                                    placeholder="Write your notes here..."
                                                    autosize={{minRows: 2, maxRows: 6}}
                                                    value={a.notes}
                                                />
                                            </Col>
                                        </Row>
                                        <Divider/>
                                    </div>)}
                                )
                            }
                        </Modal>
                    </React.Fragment>
                    : null}
                </div>
            </NoHeaderPanel>
        );
    }
}

function mapStateToProps(state) {
    console.log('what')
    return {
        assistant: state.assistant.assistant,
        appointments: state.appointment.appointments,
    };
}

export default connect(mapStateToProps)(Calendar);
