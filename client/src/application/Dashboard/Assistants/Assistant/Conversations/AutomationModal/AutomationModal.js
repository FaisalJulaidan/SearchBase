import React from 'react'
import {Checkbox, Col, Form, InputNumber, List, Modal, Switch, Tag, TimePicker} from 'antd'
import moment from 'moment';
import styles from './AutomationModal.module.less'

const FormItem = Form.Item;

class AutomationModal extends React.Component {

    state = {
        showRejectionSlide: false,
        showAcceptSlide: false,
        showSetAppointment: false,
        activeWeekDays: {
            Sunday: false,
            Monday: false,
            Tuesday: false,
            Wednesday: false,
            Thursday: false,
            Friday: false,
            Saturday: false,
        }
    };

    onRejectChange = (checked) => this.setState({showRejectionSlide: checked});
    onAcceptCahnge = (checked) => this.setState({showAcceptSlide: checked});
    onAppointmentCahnge = (checked) => this.setState({showSetAppointment: checked});

    handleActivateDay = (event, day) => this.setState((state) => state.activeWeekDays[day] = event.target.checked);

    render() {

        const TimeRange = (day) => (
            <>
                <span className={styles.TimeRange}>
                    <TimePicker defaultValue={moment('7:00', 'HH:mm')} format={'HH:mm'} minuteStep={30}
                                            disabled={!this.state.activeWeekDays[day]}/>
                </span>
                <span style={{marginRight: '5px', marginLeft: '5px'}}>-</span>
                <span className={styles.TimeRange}>
                    <TimePicker defaultValue={moment('16:00', 'HH:mm')} format={'HH:mm'} minuteStep={30}
                                          disabled={!this.state.activeWeekDays[day]}/>
                </span>
            </>
        );

        const CheckBox = (day) => (
            <Checkbox className={styles.CheckBox} onChange={event => this.handleActivateDay(event, day)}>

            </Checkbox>
        );

        const weekDays = [
            {
                day: 'Sunday',
                get input() {
                    return TimeRange(this.day)
                },
                get check() {
                    return CheckBox(this.day)
                }
            },
            {
                day: 'Monday',
                get input() {
                    return TimeRange(this.day)
                },
                get check() {
                    return CheckBox(this.day)
                }
            },
            {
                day: 'Tuesday',
                get input() {
                    return TimeRange(this.day)
                },
                get check() {
                    return CheckBox(this.day)
                }
            },
            {
                day: 'Wednesday',
                get input() {
                    return TimeRange(this.day)
                },
                get check() {
                    return CheckBox(this.day)
                }
            },
            {
                day: 'Thursday',
                get input() {
                    return TimeRange(this.day)
                },
                get check() {
                    return CheckBox(this.day)
                }
            },
            {
                day: 'Friday',
                get input() {
                    return TimeRange(this.day)
                },
                get check() {
                    return CheckBox(this.day)
                }
            },
            {
                day: 'Saturday',
                get input() {
                    return TimeRange(this.day)
                },
                get check() {
                    return CheckBox(this.day)
                }
            },
        ];

        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;

        return <Modal title="Automation Modal"
                      visible={this.props.visible}
                      onOk={this.props.handleOk}
                      width={700}
                      onCancel={this.props.handleCancel}>
            <Form layout='horizontal'>
                <FormItem
                    label="Auto Reject Applicants "
                    extra="Select the percentage to auto reject the applicants"
                    {...formItemLayout}>
                    {getFieldDecorator('reject', {
                        rules: [{}],
                    })(
                        <div style={{marginLeft: 15}}>
                            <Switch onChange={this.onRejectChange} style={{marginRight: 15}}/>
                            Less Than
                            <InputNumber min={1} max={100}
                                         formatter={value => `${value}%`}
                                         style={{marginLeft: 15}}
                                         disabled={!this.state.showRejectionSlide}/>
                        </div>
                    )}
                </FormItem>

                <FormItem
                    label="Auto Accept Applicants "
                    extra="Select the percentage to auto accept the applicants"
                    {...formItemLayout}>
                    {getFieldDecorator('accept', {
                        rules: [{}],
                    })(
                        <div style={{marginLeft: 15}}>
                            <Switch onChange={this.onAcceptCahnge} style={{marginRight: 15}}/>
                            Greater Than
                            <InputNumber min={1} max={100}
                                         formatter={value => `${value}%`}
                                         style={{marginLeft: 15}}
                                         disabled={!this.state.showAcceptSlide}/>
                        </div>
                    )}
                </FormItem>

                <FormItem
                    label="Auto Set Appointment"
                    {...formItemLayout}>
                    {getFieldDecorator('appointment', {
                        rules: [{
                            initialValue: this.state.showSetAppointment
                        }],
                    })(
                        <div style={{marginLeft: 15}}>
                            <Switch onChange={this.onAppointmentCahnge}/>
                        </div>
                    )}
                </FormItem>

                <div className={this.state.showSetAppointment ? null : styles.BlurContent }>
                    {
                        <List bordered
                              dataSource={weekDays}
                              renderItem={item => (
                                  <List.Item>
                                              <Col span={12}>
                                                  {item.check}
                                                  <Tag style={{marginTop: 6}}
                                                       color={this.state.activeWeekDays[item.day] ? 'purple' : 'grey'}>
                                                      {item.day}
                                                  </Tag>
                                              </Col>
                                              <Col span={12}>
                                                  {item.input}
                                              </Col>
                                  </List.Item>
                              )}/>
                    }
                </div>

            </Form>

            {/*Blur Effect (Hidden) */}
            <div style={{display:'none'}}>
                <svg id="svg-filter">
                    <filter id="svg-blur">
                        <feGaussianBlur in="SourceGraphic" stdDeviation="2"></feGaussianBlur>
                    </filter>
                </svg>
            </div>

        </Modal>


    }
}

export default Form.create()(AutomationModal)
