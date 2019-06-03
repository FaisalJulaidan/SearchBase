import React from 'react'
import styles from "./AutoPilotConfigs.module.less";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Button, Col, Form, Input, InputNumber, Switch, Typography} from 'antd';
import 'types/TimeSlots_Types'
import {history} from "helpers";
import TimeSlots from "./TimeSlots/TimeSlots";

const FormItem = Form.Item;

const {Title, Paragraph} = Typography;

class AutoPilotConfigs extends React.Component {

    state = {
        showRejectionSlide: false,
        showAcceptSlide: false,
        showSetAppointment: false,
    };

    componentDidMount() {
        if (!this.props.location.state)
            return history.push('/dashboard/auto_pilot')
    }

    onRejectChange = (checked) => this.setState({showRejectionSlide: checked});
    onAcceptChange = (checked) => this.setState({showAcceptSlide: checked});
    onAppointmentChange = (checked) => this.setState({showSetAppointment: checked});

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
                                label="Auto Pilot Name"
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
                                            if (autoPilotsList.some(autoPilot => autoPilot.Name === value))
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
                                label="Auto Pilot Description"
                                wrapperCol = {{span: 12}}
                            >
                                {getFieldDecorator('description', {
                                    initialValue: autoPilot.Description,
                                    rules: [{}],
                                })(
                                    <Input placeholder="Auto Pilot Description"/>
                                )}
                            </FormItem>

                            <FormItem
                                label="Auto Reject Applicants "
                                extra="Select the percentage to auto reject the applicants"
                            >
                                {getFieldDecorator('reject', {
                                    initialValue: autoPilot.RejectApplications,
                                    rules: [{}],
                                })(
                                    <div style={{marginLeft: 3}}>
                                        <Switch onChange={this.onRejectChange} style={{marginRight: 15}}/>
                                        Less Than
                                        <InputNumber min={1} max={100}
                                                     formatter={value => `${value}%`}
                                                     defaultValue={autoPilot.RejectionScore}
                                                     style={{marginLeft: 15}}
                                                     disabled={!this.state.showRejectionSlide}/>
                                    </div>
                                )}
                            </FormItem>

                            <FormItem
                                label="Auto Accept Applicants "
                                extra="Select the percentage to auto accept the applicants"
                            >
                                {getFieldDecorator('accept', {
                                    initialValue: autoPilot.AcceptApplications,
                                    rules: [{}],
                                })(
                                    <div style={{marginLeft: 3}}>
                                        <Switch onChange={this.onAcceptChange} style={{marginRight: 15}}/>
                                        Greater Than
                                        <InputNumber min={1} max={100}
                                                     defaultValue={autoPilot.AcceptanceScore}
                                                     formatter={value => `${value}%`}
                                                     style={{marginLeft: 15}}
                                                     disabled={!this.state.showAcceptSlide}/>
                                    </div>
                                )}
                            </FormItem>

                            <FormItem
                                label="Auto Set Appointment"
                            >
                                {getFieldDecorator('appointment', {
                                    initialValue: autoPilot.SendCandidatesAppointments,
                                    rules: [],
                                })(
                                    <div style={{marginLeft: 3}}>
                                        <Switch onChange={this.onAppointmentChange}
                                                checked={this.state.showSetAppointment}/>
                                    </div>
                                )}
                            </FormItem>

                            <TimeSlots getFieldDecorator={getFieldDecorator}
                                       autoPilot={autoPilot}
                                       layout={layout}
                                       showSetAppointment={this.state.showSetAppointment}/>

                            <br/>

                            <Col span={16} offset={4}>
                                <Button type={'primary'}>Update Auto Pilot</Button>
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
