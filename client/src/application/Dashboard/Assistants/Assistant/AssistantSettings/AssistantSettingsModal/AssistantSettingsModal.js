import React, {Component} from 'react';
import {Button, Form, Input, InputNumber, Modal, Slider, Switch} from "antd";

const FormItem = Form.Item;


class AssistantSettingsModal extends Component {
    state = {
        isPopupDisabled: this.props.assistant.SecondsUntilPopup <= 0,
        isAlertsEnabled: this.props.assistant.MailEnabled,
        alertOptions: {0: "Immediately", 4: "4 hours", 8: "8 hours", 12: "12 hours", 24: "24 hours"}
    };

    togglePopupSwitch = () => {
        this.setState({isPopupDisabled: !this.state.isPopupDisabled})
    };

    toggleAlertsSwitch = () => {
        this.setState({isAlertsEnabled: !this.state.isAlertsEnabled})
    };


    componentDidMount() {
        this.setState({
            inputValue: this.props.assistant.SecondsUntilPopup
        });
    }

    handleSave = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                if (this.state.isPopupDisabled) {
                    values.secondsUntilPopup = 0
                }
                values["alertsEnabled"] = this.state.isAlertsEnabled;

                this.props.handleSave(values)
            }
        });
    };

    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };

        const alertsKeys = Object.keys(this.state.alertOptions);
        const maxAlertsLength = parseInt(alertsKeys[alertsKeys.length - 1]);

        const {getFieldDecorator} = this.props.form;
        const {assistant} = this.props;

        const {inputValue} = this.state;

        return (
            <Modal
                title="Edit Assistant"
                visible={this.props.visible}
                width={800}
                destroyOnClose={true}
                onCancel={this.props.handleCancel}
                footer={[
                    <Button key="delete" type="danger" onClick={this.props.handleDelete}>
                        Delete
                    </Button>,
                    <Button key="cancel" onClick={this.props.handleCancel}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleSave}>
                        Save
                    </Button>,
                ]}>

                <Form layout='horizontal'>
                    <FormItem
                        label="Assistant Name"
                        extra="Enter a name for your assistant to easily identify it in the dashboard"
                        {...formItemLayout}>
                        {
                            getFieldDecorator('assistantName', {
                                initialValue: assistant.Name,
                                rules: [{
                                    required: true,
                                    message: 'Please input your assistant name',
                                }],
                            })
                            (<Input placeholder="Ex: My first assistant, Sales Assistant"/>)
                        }
                    </FormItem>

                    <FormItem
                        label="Welcome Message"
                        extra="This will be sent as first message"
                        {...formItemLayout}>

                        {
                            getFieldDecorator('welcomeMessage', {
                                initialValue: assistant.Message,
                                rules: [{
                                    required: true,
                                    message: 'Please input your welcome message',
                                }],
                            })(
                                <Input placeholder="Ex: Hey there, Welcome visitor"/>
                            )
                        }
                    </FormItem>

                    <FormItem
                        label="Header Title"
                        extra="This will apear on top of your chatbot"
                        {...formItemLayout}>
                        {
                            getFieldDecorator('topBarTitle', {
                                initialValue: assistant.TopBarText,
                                rules: [{
                                    required: true,
                                    message: 'Please input your header title',
                                }],
                            })(
                                <Input placeholder="Ex: Recruiter Bot"/>
                            )
                        }
                    </FormItem>

                    <FormItem
                        {...formItemLayout}
                        label="Time to Popup"
                        extra="This will enforce the assistants' (chatbot) to popup automatically"
                    >
                        <Switch checked={!this.state.isPopupDisabled} onChange={this.togglePopupSwitch}
                                style={{marginRight: '5px'}}/>
                        {getFieldDecorator('secondsUntilPopup', {initialValue: assistant.SecondsUntilPopup === 0 ? 1 : assistant.SecondsUntilPopup})(
                            <InputNumber disabled={this.state.isPopupDisabled} min={1}/>
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
                            initialValue: this.props.assistant.MailPeriod
                        })(
                            <Slider
                                max={maxAlertsLength}
                                disabled={!this.state.isAlertsEnabled}
                                marks={this.state.alertOptions} step={null}/>
                        )}
                    </FormItem>

                 </Form>
            </Modal>
        );
    }
}

export default Form.create()(AssistantSettingsModal)