import React from 'react'
import {Form, InputNumber, Modal, Switch} from 'antd'
import TimeSlots from './TimeSlots/TimeSlots'

const FormItem = Form.Item;

class AutomationModal extends React.Component {

    state = {
        showRejectionSlide: false,
        showAcceptSlide: false,
        showSetAppointment: false,
    };

    onRejectChange = (checked) => this.setState({showRejectionSlide: checked});
    onAcceptCahnge = (checked) => this.setState({showAcceptSlide: checked});
    onAppointmentCahnge = (checked) => this.setState({showSetAppointment: checked});

    render() {



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
                        <div style={{marginLeft: 3}}>
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
                        <div style={{marginLeft: 3}}>
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
                        initialValue: this.state.showSetAppointment,
                        rules: [],
                    })(
                        <div style={{marginLeft: 3}}>
                            <Switch onChange={this.onAppointmentCahnge} checked={this.state.showSetAppointment}/>
                        </div>
                    )}
                </FormItem>

                <TimeSlots getFieldDecorator={getFieldDecorator}
                           showSetAppointment={this.state.showSetAppointment}/>

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
