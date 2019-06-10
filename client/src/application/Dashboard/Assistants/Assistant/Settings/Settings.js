import React, {Component} from 'react';
import {connect} from 'react-redux';
import {store} from "store/store";

import {Button, Select, Form, Input, InputNumber, Divider, Slider, Switch, Modal, Radio} from "antd";
import {assistantActions, crmActions} from "store/actions";
import {history} from "helpers";

import countries from 'helpers/static_data/countries'
const FormItem = Form.Item;
const Option = Select.Option;
const confirm = Modal.confirm;

const manualNotify = [null, 0, 6, 24, 168]


class Settings extends Component {
    state = {
        isPopupDisabled: this.props.assistant.SecondsUntilPopup <= 0,
        isAlertsEnabled: this.props.assistant.MailEnabled,
        // alertOptions: {0: "Immediately", 4: "4 hours", 8: "8 hours", 12: "12 hours", 24: "24 hours"}
        alertOptions: {0: "Immediately"},
        isManualNotify: manualNotify.indexOf(this.props.assistant.NotifyEvery) === -1
    };

    componentDidMount() {
        this.setState({
            inputValue: this.props.assistant.SecondsUntilPopup
        });
    }


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



    handleSave = () => this.props.form.validateFields((err, values) => {
        console.log(err)
        console.log(values)
        console.log('kekistan')
        if (!err) {
            if (this.state.isPopupDisabled)
                values.secondsUntilPopup = 0;
                values.alertsEnabled = this.state.isAlertsEnabled;
                values.config = {
                restrictedCountries: values.restrictedCountries || []
            };
            delete values.restrictedCountries;
            store.dispatch(assistantActions.updateAssistantConfigs(this.props.assistant.ID, values))
        }
    });

    handleDelete = () => {
        confirm({
            title: `Delete assistant confirmation`,
            content: `If you click OK, this assistant will be deleted with its content forever`,
            onOk: () => {
                this.props.dispatch(assistantActions.deleteAssistant(this.props.assistant.ID))
                    .then(() => history.push('/dashboard/assistants'));
            }
        });
    };

    render() {
        const alertsKeys = Object.keys(this.state.alertOptions);
        const maxAlertsLength = parseInt(alertsKeys[alertsKeys.length - 1]);
        const {isManualNotify} = this.state;
        const {getFieldDecorator} = this.props.form;
        const {assistant} = this.props;

        const countriesOptions = [...countries.map(country => <Option key={country.code}>{country.name}</Option>)];

        return (
            <>
                <Form layout='vertical' wrapperCol={{span: 12}}>

                    <h2> Basic Settings:</h2>
                    <FormItem
                        label="Assistant Name"
                        extra="Enter a name for your assistant to easily identify it in the dashboard"
                    >
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
                        label="Description"
                        extra="Enter a description for your assistant to easily identify it in the dashboard">
                        {
                            getFieldDecorator('assistantDesc', {
                                initialValue: assistant?.Description,
                                rules: [{
                                    required: false,
                                    message: 'Please input your assistant description'
                                }]
                            })
                            (<Input placeholder="Ex: Qualify candidates for sales job"/>)
                        }
                    </FormItem>

                    <FormItem
                        label="Introduction Message"
                        extra="This will be sent as first message"
                    >

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
                    >
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
                    <Button type={'primary'} onClick={this.handleSave}>Save changes</Button>

                    {/* ================================ */}
                    <br />
                    <Divider/>
                    <h2> Advanced Settings:</h2>

                    <FormItem
                        label="Pop up after"
                        extra="This will make your chatbot pop up automatically on your website"
                    >
                        <Switch checked={!this.state.isPopupDisabled} onChange={this.togglePopupSwitch}
                                style={{marginRight: '15px'}}/>
                        {getFieldDecorator('secondsUntilPopup', {initialValue: assistant.SecondsUntilPopup === 0 ? 1 : assistant.SecondsUntilPopup})(
                            <InputNumber disabled={this.state.isPopupDisabled} min={1}/>
                        )}
                        <span className="ant-form-text"> seconds</span>
                    </FormItem>


                    {isManualNotify ?
                        <Form.Item label="Alert Me Every:"
                                  extra="Select how often you would like to be notified via email of new chats">
                            <Radio.Group style={{width:'100%'}}>
                                <Radio.Button value={null} disabled={isManualNotify}>Never</Radio.Button>
                                <Radio.Button value={0} disabled={isManualNotify}>Immediately</Radio.Button>
                                <Radio.Button value={6} disabled={isManualNotify}>Every 6hrs</Radio.Button>
                                <Radio.Button value={24} disabled={isManualNotify}>Daily</Radio.Button>
                                <Radio.Button value={168} disabled={isManualNotify}>Weekly</Radio.Button>
                                <Radio.Button onClick={() => {this.setState({isManualNotify: !isManualNotify})}}>Custom</Radio.Button>
                            </Radio.Group>
                            {getFieldDecorator('notifyEvery', {
                                    initialValue: assistant.NotifyEvery,
                                rules: [{
                                    required: true,
                                    message: 'Please type in a number of hours',
                            }],
                            })(
                                <Input placeholder="Amount of time between notifications, in hours"/>
                            )}
                        </Form.Item>
                    :
                        <Form.Item label="Alert Me Every:"
                                   extra="Select how often you would like to be notified via email of new chats">
                            {getFieldDecorator('notifyEvery', {
                                initialValue: assistant.NotifyEvery === null ? "null" : assistant.NotifyEvery,
                                rules: [{
                                    required: true,
                                    message: 'Please select how often or never',
                                }],
                            })(
                                <Radio.Group style={{width:'100%'}}>
                                    <Radio.Button value={"null"} disabled={isManualNotify}>Never</Radio.Button>
                                    <Radio.Button value={0} disabled={isManualNotify}>Immediately</Radio.Button>
                                    <Radio.Button value={6} disabled={isManualNotify}>Every 6hrs</Radio.Button>
                                    <Radio.Button value={24} disabled={isManualNotify}>Daily</Radio.Button>
                                    <Radio.Button value={168} disabled={isManualNotify}>Weekly</Radio.Button>
                                    <Radio.Button onClick={() => {this.setState({isManualNotify: !isManualNotify})}}>Custom</Radio.Button>
                                </Radio.Group>
                            )}
                        </Form.Item>}
                    <FormItem
                        label="Restricted Countries"
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


                    {/*<FormItem*/}
                        {/*label="Records Notifications"*/}
                        {/*extra="If you turn this on, we will notify you through your email"*/}
                    {/*>*/}
                        {/*<Switch checked={this.state.isAlertsEnabled} onChange={this.toggleAlertsSwitch}*/}
                                {/*style={{marginRight: '5px'}}/>*/}
                    {/*</FormItem>*/}

                    {/*<FormItem*/}
                        {/*label="Alert Me Every:"*/}
                        {/*extra="Select how often you would like to be notified"*/}
                    {/*>*/}
                        {/*{getFieldDecorator('alertEveryy', {*/}
                            {/*initialValue: this.props.assistant.MailPeriod*/}
                        {/*})(*/}
                            {/*<Slider*/}
                                {/*max={maxAlertsLength}*/}
                                {/*disabled={!this.state.isAlertsEnabled}*/}
                                {/*marks={this.state.alertOptions} step={null}/>*/}
                        {/*)}*/}
                    {/*</FormItem>*/}







                    <Button type={'primary'} onClick={this.handleSave}>Save changes</Button>
                </Form>

                <br />
                <Divider/>
                <h2> Delete Assistant:</h2>
                <Button type={'danger'} onClick={this.handleDelete}>Delete</Button>

            </>
        );
    }
}

function mapStateToProps(state) {
    return {};
}

export default connect(mapStateToProps)(Form.create()(Settings));