import React from 'react'
import styles from "./AutoPilotConfigs.module.less";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Button, Col, Form, Input, InputNumber, Switch, Typography, Divider} from 'antd';
import 'types/TimeSlots_Types'
import {history} from "helpers";
import TimeSlots from "./TimeSlots/TimeSlots";
import {autoPilotActions} from "store/actions";
import {store} from "store/store";

const FormItem = Form.Item;

const {Title, Paragraph} = Typography;

class AutoPilotConfigs extends React.Component {

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
        if (!this.props.location.state)
            return history.push('/dashboard/auto_pilot');

        const /**@type AutoPilot*/ autoPilot = this.props.location.state?.autoPilot || {};
        this.setState({
            rejectApplications: autoPilot.RejectApplications,
            acceptApplications: autoPilot.AcceptApplications,
            sendAcceptanceEmail: autoPilot.SendAcceptanceEmail,
            sendRejectionEmail: autoPilot.SendRejectionEmail,
            sendCandidatesAppointments: autoPilot.SendCandidatesAppointments,
            acceptanceScore: autoPilot.AcceptanceScore * 100,
            rejectionScore: autoPilot.RejectionScore * 100
        })
    }

    onRejectChange = (checked) => this.setState({rejectApplications: checked});
    onAcceptChange = (checked) => this.setState({acceptApplications: checked});
    onAppointmentChange = (checked) => this.setState({sendCandidatesAppointments: checked});
    onSendAcceptanceEmailChange = (checked) => this.setState({sendAcceptanceEmail: checked});
    onSendRejectionEmailChange = (checked) => this.setState({sendRejectionEmail: checked});

    changeScore = (value, stateName) => this.setState(state => state[stateName] = value);

    onSubmit = () => this.props.form.validateFields((err, values) => {
        const /**@type AutoPilot*/ autoPilot = this.props.location.state?.autoPilot || {};
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

            openTimeSlots: weekDays
        };

        store.dispatch(autoPilotActions.updateAutoPilot(autoPilot.ID, payload));
    });

    render() {
        const /**@type AutoPilot*/ autoPilot = this.props.location.state?.autoPilot || {};
        const layout = {
            labelCol: {span: 4},
            wrapperCol: {span: 16},
        };
        const {getFieldDecorator} = this.props.form;
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Title}>
                        <div className={styles.Details}>
                            <Title>{autoPilot.Name}</Title>
                            <Paragraph type="secondary">
                                {autoPilot.Description}
                            </Paragraph>
                        </div>
                    </div>

                    <div className={styles.Body}>
                        <Form layout='vertical' style={{width: '100%'}}>
                            <FormItem
                                label="Auto pilot name"
                                wrapperCol = {{span: 12}}
                                >
                                {getFieldDecorator('name', {
                                    initialValue: autoPilot.Name,
                                    rules: [{
                                        required: true,
                                        message: "Please add name or the name you entered is duplicated",
                                        validator: (_, value, callback) => {
                                            // check if the value equals any of the name from
                                            // this.props.autoPilotsSlots
                                            // if there is an error return the callback with the message
                                            const { /**@type AutoPilot[]*/ autoPilotsList} = this.props;
                                            if (autoPilotsList?.some(autoPilot => autoPilot.Name === value))
                                                return callback(value + ' is duplicated');
                                            else
                                                return callback()
                                        }
                                    }],
                                })(
                                    <Input placeholder="Auto Pilot Name"/>
                                )}
                            </FormItem>

                            <FormItem
                                label="Auto pilot description"
                                wrapperCol = {{span: 12}}
                            >
                                {getFieldDecorator('description', {
                                    initialValue: autoPilot.Description,
                                    rules: [{}],
                                })(
                                    <Input placeholder="Auto Pilot Description"/>
                                )}
                            </FormItem>

                            <Divider/>
                            <br />
                            <h2> Applications Acceptance Automation:</h2>
                            <FormItem label="Auto accept applicants "
                                      help="Select the percentage to auto accept the applicants">
                                {getFieldDecorator('acceptApplications', {
                                    valuePropName: 'checked',
                                })(
                                    <>
                                        <Switch onChange={this.onAcceptChange} style={{marginRight: 15}}
                                                defaultChecked={autoPilot.AcceptApplications}/>
                                        Greater Than
                                        <InputNumber min={0} max={100}
                                                     onChange={value => this.changeScore(value, 'acceptanceScore')}
                                                     defaultValue={this.state.acceptanceScore}
                                                     key={this.state.acceptanceScore ? 'notLoadedYet' : 'loaded'}
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
                                    initialValue: autoPilot.SendAcceptanceEmail,
                                    rules: [],
                                })(
                                    <div style={{marginLeft: 3}}>
                                        <Switch onChange={this.onSendAcceptanceEmailChange}
                                                checked={this.state.sendAcceptanceEmail}/>
                                    </div>
                                )}
                            </FormItem>



                            <Divider/>
                            <br />
                            <h2> Applications Rejection Automation:</h2>
                            <Form.Item label="Auto reject applicants "
                                       help="Select the percentage to auto reject the applicants">
                                {getFieldDecorator('rejectApplications', {
                                    valuePropName: 'checked',
                                })(
                                    <>
                                        <Switch onChange={this.onRejectChange} style={{marginRight: 15}}
                                                defaultChecked={autoPilot.RejectApplications}/>
                                        Less Than
                                        <InputNumber min={1} max={100}
                                                     onChange={value => this.changeScore(value, 'rejectionScore')}
                                                     formatter={value => `${value}%`}
                                                     key={this.state.acceptanceScore ? 'notLoadedYet' : 'loaded'}
                                                     defaultValue={this.state.rejectionScore}
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

                            <Divider/>
                            <br />
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

                            <Col span={16} offset={4}>
                                <Button type={'primary'} onClick={this.onSubmit}>Update Auto Pilot</Button>
                            </Col>


                            <br/>
                            <br/>
                        </Form>


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

export default Form.create()(AutoPilotConfigs)
