import React, {Component} from 'react';

import {Button, Form, Input, Modal, Select, InputNumber, message, Switch, Slider} from 'antd';
import {connect} from "react-redux";
import {assistantActions} from "../../../../store/actions";

const FormItem = Form.Item;
const Option = Select.Option;


const loading = () => {
    message.loading('Adding assistant', 0);
};

class NewAssistantModal extends Component {

    state = {
        isPopupDisabled: true,
        isAlertsEnabled: false,
        alertOptions: {0: "Immediately", 4: "4 hours", 8: "8 hours", 12: "12 hours", 24: "24 hours"}
    };

    togglePopupSwitch = () => {
        this.setState({isPopupDisabled: !this.state.isPopupDisabled})
    };

    toggleAlertsSwitch = () => {
        this.setState({isAlertsEnabled: !this.state.isAlertsEnabled})
    };

    handleAdd = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                if(this.state.isPopupDisabled) {values.secondsUntilPopup = 0}
                values["alertsEnabled"] = this.state.isAlertsEnabled;
                console.log(values);
                // send to server
                this.props.dispatch(assistantActions.addAssistant(values));
                loading();
            }
        });
    };

    componentDidUpdate(prevProps) {
        if (!this.props.isAdding && this.props.isAdding !== prevProps.isAdding) {
            this.props.hideModal();
            message.destroy();
            message.success(this.props.successMsg)
        }
    }


    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };

        const alertsKeys = Object.keys(this.state.alertOptions);
        const maxAlertsLength = parseInt(alertsKeys[alertsKeys.length - 1]);

        const {getFieldDecorator} = this.props.form;

        return (
            <Modal
                width={800}
                title="Create New Assistant"
                visible={this.props.visible}
                onCancel={this.props.hideModal}
                destroyOnClose={true}
                footer={[
                    <Button key="cancel" onClick={this.props.hideModal}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleAdd}>
                        Add
                    </Button>,
                ]}>
                <Form layout='horizontal'>
                    <FormItem
                        label="Assistant Name"
                        extra="Enter a name for your assistant to easily identify it in the dashboard"
                        {...formItemLayout}>
                        {getFieldDecorator('assistantName', {
                            rules: [{
                                required: true,
                                message: 'Please input your assistant name',
                            }],
                        })(
                            <Input placeholder="Ex: My first assistant, Sales Assistant"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Welcome Message"
                        extra="This will be sent as first message"
                        {...formItemLayout}>
                        {getFieldDecorator('welcomeMessage', {
                            rules: [{
                                required: true,
                                message: 'Please input your welcome message',
                            }],
                        })(
                            <Input placeholder="Ex: Hey there, Welcome visitor"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Header Title"
                        extra="This will apear on top of your chatbot"
                        {...formItemLayout}>
                        {getFieldDecorator('topBarTitle', {
                            rules: [{
                                required: true,
                                message: 'Please input your header title',
                            }],
                        })(
                            <Input placeholder="Ex: Recruiter Bot"/>
                        )}
                    </FormItem>

                    <FormItem
                    {...formItemLayout}
                    label="Time to Popup"
                    extra="This will enforce the assistants' (chatbot) to popup automatically"
                    >
                    <Switch defaultChecked={false} onChange={this.togglePopupSwitch} style={{marginRight: '5px'}} />
                    {getFieldDecorator('secondsUntilPopup', { initialValue: 1 })(
                        <InputNumber disabled={this.state.isPopupDisabled} min={1} />
                    )}
                    <span className="ant-form-text"> seconds</span>
                    </FormItem>

                    <FormItem
                        {...formItemLayout}
                        label="New Record Alert"
                        extra="Turning this on will make the assistant alert you when it has been used"
                    >
                        <Switch checked={this.state.isAlertsEnabled} onChange={this.toggleAlertsSwitch}
                                style={{marginRight: '5px'}}/>
                    </FormItem>

                    <FormItem
                        {...formItemLayout}
                        label="Alerts Every:"
                        extra="Select in what period of time the bot to check for new records and alert you. Note: 'Immediately' could spam your email if your assistant is used a lot"
                    >
                        {getFieldDecorator('alertEvery', {
                            initialValue: parseInt(alertsKeys[alertsKeys.length - 2])
                        })(
                            <Slider
                                max={maxAlertsLength}
                                disabled={!this.state.isAlertsEnabled}
                                marks={this.state.alertOptions} step={null}/>
                        )}
                    </FormItem>

                    <FormItem {...formItemLayout}
                              label="Assistant Template">

                        {
                            getFieldDecorator('template')(
                                <Select placeholder="Please select template">
                                    <Option value="recruitment">Recruitment</Option>
                                    <Option value="Shopping">Shopping</Option>
                                    <Option value="Sales">Sales</Option>
                                </Select>
                            )
                        }
                    </FormItem>
                </Form>
            </Modal>
        );
    }
}

function mapStateToProps(state) {
    return {
        successMsg: state.assistant.successMsg,
        isAdding: state.assistant.isAdding
    };
}

export default connect(mapStateToProps)(Form.create()(NewAssistantModal))
