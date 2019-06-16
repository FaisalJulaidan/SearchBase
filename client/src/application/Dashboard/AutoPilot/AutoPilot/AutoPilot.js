import React from 'react'
import {connect} from 'react-redux';
import styles from "./AutoPilot.module.less";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Button, Form, Input, InputNumber, Switch, Typography, Divider, Spin, Modal, Breadcrumb} from 'antd';
import 'types/TimeSlots_Types'
import {history} from "helpers";
import TimeSlots from "./TimeSlots/TimeSlots";
import {autoPilotActions} from "store/actions";

const FormItem = Form.Item;
const confirm = Modal.confirm;

const {Title, Paragraph} = Typography;

class AutoPilot extends React.Component {

    constructor(props) {
        super(props);
        this.TimeSlotsRef = React.createRef();
    }
    state = {
        rejectApplications: false,
        acceptApplications: false,
        sendAcceptanceEmail: false,
        sendRejectionEmail: false,
        sendCandidatesAppointments: false,

        acceptanceScore: null,
        rejectionScore: null
    };


    componentDidMount() {

        this.props.dispatch(autoPilotActions.fetchAutoPilot(this.props.match.params.id))
            .then(()=> {
                const {autoPilot} = this.props;
                this.setState({
                    rejectApplications: autoPilot.RejectApplications,
                    acceptApplications: autoPilot.AcceptApplications,
                    sendAcceptanceEmail: autoPilot.SendAcceptanceEmail,
                    sendRejectionEmail: autoPilot.SendRejectionEmail,
                    sendCandidatesAppointments: autoPilot.SendCandidatesAppointments,
                    acceptanceScore: autoPilot.AcceptanceScore * 100,
                    rejectionScore: autoPilot.RejectionScore * 100
                })
            }).catch(() => history.push(`/dashboard/auto_pilots`));


    }

    onRejectChange = (checked) => this.setState({rejectApplications: checked});
    onAcceptChange = (checked) => this.setState({acceptApplications: checked});
    onAppointmentChange = (checked) => this.setState({sendCandidatesAppointments: checked});
    onSendAcceptanceEmailChange = (checked) => this.setState({sendAcceptanceEmail: checked});
    onSendRejectionEmailChange = (checked) => this.setState({sendRejectionEmail: checked});

    handleDelete = () => {
        confirm({
            title: `Delete auto pilot confirmation`,
            content: `If you click OK, this auto pilot will be deleted and disconnected from all assistants that are connected to it`,
            onOk: () => {
                console.log(this.props);
                this.props.dispatch(autoPilotActions.deleteAutoPilot(this.props.autoPilot.ID))
                    .then(() => history.push('/dashboard/auto_pilots'));
            }
        });
    };

    onSubmit = () => this.props.form.validateFields((err, values) => {
        const /**@type AutoPilot*/ autoPilot = this.props.autoPilot || {};
        const {state, TimeSlotsRef} = this;
        const timeSlots = TimeSlotsRef.current.state.weekDays;

        let weekDays = [];
        for (let i = 0; i < 7; i++) {
            weekDays.push({
                day: i,
                from: [timeSlots[i].from.hours(), timeSlots[i].from.minutes()],
                to: [timeSlots[i].to.hours(), timeSlots[i].to.minutes()],
                duration: +TimeSlotsRef.current.state.duration.split('min')[0],
                active: timeSlots[i].active
            })
        }

        let payload = {
            active: autoPilot.Active,
            name: values.name,
            description: values.description,
            acceptApplications: state.acceptApplications,
            rejectApplications: state.rejectApplications,
            sendAcceptanceEmail: state.sendAcceptanceEmail,
            sendRejectionEmail: state.sendRejectionEmail,
            acceptanceScore: state.acceptanceScore / 100,
            rejectionScore: state.rejectionScore / 100,
            sendCandidatesAppointments: state.sendCandidatesAppointments,

            openTimes: weekDays
        };

        this.props.dispatch(autoPilotActions.updateAutoPilotConfigs(autoPilot.ID, payload));
    });

    render() {
        const /**@type AutoPilot*/ autoPilot = this.props.autoPilot;
        const layout = {
            labelCol: {span: 4},
            wrapperCol: {span: 16},
        };
        const {getFieldDecorator} = this.props.form;
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <div style={{marginBottom: 20}}>
                            <Breadcrumb>
                                <Breadcrumb.Item>
                                    <a href={"javascript:void(0);"}
                                       onClick={() => history.push('/dashboard/auto_pilots')}>
                                        Auto Pilots
                                    </a>
                                </Breadcrumb.Item>
                                <Breadcrumb.Item>{autoPilot?.Name}</Breadcrumb.Item>
                            </Breadcrumb>
                        </div>

                        <div className={styles.Title}>
                            <Title>{autoPilot?.Name}</Title>
                            <Paragraph type="secondary">
                                {autoPilot?.Description}
                            </Paragraph>
                        </div>
                    </div>

                    <div className={styles.Body}>
                        {!autoPilot ? <Spin/> :
                            <Form layout='vertical' wrapperCol = {{span: 12}} style={{width: '100%'}}>
                                <FormItem
                                    label="Name"
                                    >
                                    {getFieldDecorator('name', {
                                        initialValue: autoPilot.Name,
                                        rules: [
                                            {required: true, message: "Enter a name for your auto pilot"},
                                            {validator: (_, value, callback) => {
                                                // check if the value equals any of the name from
                                                // this.props.autoPilotsSlots
                                                // if there is an error return the callback with the message
                                                if (this.props.autoPilotsList?.some(autoPilot => autoPilot.Name === value
                                                    && this.props.autoPilot.Name !== value))
                                                    return callback(value + ' is duplicated');
                                                else
                                                    return callback()
                                                }
                                            }
                                        ],
                                    })(
                                        <Input placeholder="Auto Pilot Name"/>
                                    )}
                                </FormItem>

                                <FormItem
                                    label="Description"
                                >
                                    {getFieldDecorator('description', {
                                        initialValue: autoPilot?.Description,
                                        rules: [{}],
                                    })(
                                        <Input placeholder="Auto Pilot Description"/>
                                    )}
                                </FormItem>

                                <br />
                                <Button type={'primary'} onClick={this.onSubmit}>Save changes</Button>

                                <br />
                                <Divider/>
                                <h2> Applications Acceptance Automation:</h2>
                                <FormItem label="Auto accept applicants "
                                          help="Select the percentage to auto accept the applicants">
                                    {getFieldDecorator('acceptApplications', {
                                        valuePropName: 'checked',
                                    })(
                                        <>
                                            <Switch onChange={this.onAcceptChange}
                                                    style={{marginRight: 15}}
                                                    checked={this.state.acceptApplications}
                                            />
                                            A score greater than
                                            <InputNumber min={0} max={100}
                                                         onChange={value => this.setState({acceptanceScore: value})}
                                                         value={this.state.acceptanceScore}
                                                         key={autoPilot?.AcceptanceScore ? 'notLoadedYet' : 'loaded'}
                                                         formatter={value => `${value}%`}
                                                         style={{marginLeft: 15}}
                                                         disabled={!this.state.acceptApplications}/>
                                        </>
                                    )}
                                </FormItem>

                                <FormItem label="Auto send acceptance emails"
                                          help="Accepted applicants will be notified via email if email is provided (candidates applications only)"
                                >
                                    {getFieldDecorator('sendAcceptanceEmail', {
                                        initialValue: autoPilot?.SendAcceptanceEmail,
                                        rules: [],
                                    })(
                                        <div style={{marginLeft: 3}}>
                                            <Switch onChange={this.onSendAcceptanceEmailChange}
                                                    checked={this.state.sendAcceptanceEmail}
                                            />
                                        </div>
                                    )}
                                </FormItem>

                                <br />
                                <Button type={'primary'} onClick={this.onSubmit}>Save changes</Button>

                                <br />
                                <Divider/>
                                <h2> Applications Rejection Automation:</h2>
                                <Form.Item label="Auto reject applicants "
                                           help="Select the percentage to auto reject the applicants">
                                    {getFieldDecorator('rejectApplications', {
                                        valuePropName: 'checked',
                                    })(
                                        <>
                                            <Switch onChange={this.onRejectChange} style={{marginRight: 15}}
                                                    checked={this.state.rejectApplications}/>
                                            A score less than
                                            <InputNumber min={1} max={100}
                                                         onChange={value => this.setState({rejectionScore: value})}
                                                         formatter={value => `${value}%`}
                                                         key={autoPilot?.RejectionScore ? 'notLoadedYet' : 'loaded'}
                                                         value={this.state.rejectionScore}
                                                         style={{marginLeft: 15}}
                                                         disabled={!this.state.rejectApplications}/>
                                        </>
                                    )}
                                </Form.Item>

                                <FormItem label="Auto send rejection emails"
                                          help="Rejected applicants will be notified via email if email is provided (candidates applications only)">
                                    {getFieldDecorator('sendRejectionEmail', {
                                        initialValue: autoPilot.SendRejectionEmail,
                                        rules: [],
                                    })(
                                        <div style={{marginLeft: 3}}>
                                            <Switch onChange={this.onSendRejectionEmailChange}
                                                    checked={this.state.sendRejectionEmail}/>
                                        </div>
                                    )}
                                </FormItem>

                                <br />
                                <Button type={'primary'} onClick={this.onSubmit}>Save changes</Button>

                                <br />
                                <Divider/>
                                <h2> Manage Appointments Automation:</h2>
                                <FormItem label="Auto manage candidates appointments"
                                          help="Accepted candidates will receive an email (if provided) to pick a time slot"

                                >
                                    {getFieldDecorator('sendCandidatesAppointments', {
                                        initialValue: autoPilot.SendCandidatesAppointments,
                                        rules: [],
                                    })(
                                        <div style={{marginLeft: 3}}>
                                            <Switch onChange={this.onAppointmentChange}
                                                    checked={this.state.sendCandidatesAppointments}/>
                                        </div>
                                    )}
                                </FormItem>

                                <TimeSlots ref={this.TimeSlotsRef}
                                           getFieldDecorator={getFieldDecorator}
                                           autoPilot={autoPilot}
                                           layout={layout}
                                           showSetAppointment={this.state.sendCandidatesAppointments}/>



                                <br/>
                                <br/>
                                <Button type={'primary'} onClick={this.onSubmit}>Save changes</Button>

                            </Form>
                        }

                        <br />
                        <Divider/>
                        <Button type={'danger'} size={'large'} onClick={this.handleDelete}>Delete Auto Pilot</Button>

                        {/*Blur Effect (Hidden) */}
                        <div style={{display: 'none'}}>
                            <svg id="svg-filter">
                                <filter id="svg-blur">
                                    <feGaussianBlur in="SourceGraphic" stdDeviation="2"></feGaussianBlur>
                                </filter>
                            </svg>
                        </div>

                    </div>
                </NoHeaderPanel>
            </>
        )
    }
}

function mapStateToProps(state) {
    return {
        autoPilot: state.autoPilot.autoPilot,
        autoPilotsList: state.autoPilot.autoPilotsList,
        isLoading: state.autoPilot.isLoading,
    };
}

export default connect(mapStateToProps)(Form.create()(AutoPilot));
