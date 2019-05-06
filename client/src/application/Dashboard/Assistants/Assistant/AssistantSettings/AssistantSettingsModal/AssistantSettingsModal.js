import React, {Component} from 'react';
import {Button, Select, Form, Input, InputNumber, Modal, Slider, Switch} from "antd";
import countries from 'helpers/static_data/countries'
const FormItem = Form.Item;
const Option = Select.Option;

class AssistantSettingsModal extends Component {
    state = {
        isPopupDisabled: this.props.assistant.SecondsUntilPopup <= 0,
        isAlertsEnabled: this.props.assistant.MailEnabled,
        alertOptions: {0: "Immediately", 4: "4 hours", 8: "8 hours", 12: "12 hours", 24: "24 hours"}
    };

    checkName = (rule, value, callback) => {
        if (!this.props.isAssistantNameValid(value) && this.props.assistant.Name !== value) {
            callback('Assistant name already exists. Choose another one, please!');
        } else {
            callback();
        }
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

    handleSave = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            if (this.state.isPopupDisabled)
                values.secondsUntilPopup = 0;
                values.alertsEnabled = this.state.isAlertsEnabled;
                values.config = {
                restrictedCountries: values.restrictedCountries || []
            };
            delete values.restrictedCountries;
            this.props.handleSave(values)
        }
    });

    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };

        const alertsKeys = Object.keys(this.state.alertOptions);
        const maxAlertsLength = parseInt(alertsKeys[alertsKeys.length - 1]);

        const {getFieldDecorator} = this.props.form;
        const {assistant} = this.props;

        const countriesOptions = [...countries.map(country => <Option key={country.code}>{country.name}</Option>)];

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
                                rules: [
                                    {required: true, message: 'Please input your assistant name'},
                                    {validator: this.checkName}
                                ]
                            })
                            (<Input placeholder="Recruitment Chatbot"/>)
                        }
                    </FormItem>

                    <FormItem
                        label="Introduction Message"
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
                        extra="This will appear on top of your Chatbot"
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
                        label="Pop up"
                        extra="This will make your chatbot pop up automatically on your website"
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
                        label="Records Notifications"
                        extra="If you turn this on, we will notify you through your email"
                    >
                        <Switch checked={this.state.isAlertsEnabled} onChange={this.toggleAlertsSwitch}
                                style={{marginRight: '5px'}}/>
                    </FormItem>

                    <FormItem
                        {...formItemLayout}
                        label="Restricted Contries"
                        extra="Chatbot will be disabled for users who live in the selected countries"
                    >
                        {
                            getFieldDecorator('restrictedCountries', {
                                initialValue: assistant.Config?.restrictedCountries,
                            })(
                                <Select mode="multiple" style={{width: '100%'}}
                                        filterOption={(inputValue, option) => option.props.children.toLowerCase().includes(inputValue.toLowerCase())}
                                        placeholder="Please select country or countries">
                                    {countriesOptions}
                                </Select>
                            )
                        }
                    </FormItem>

                    <FormItem
                        {...formItemLayout}
                        label="Alert Me Every:"
                        extra="Select how often you would like to be notified"
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
