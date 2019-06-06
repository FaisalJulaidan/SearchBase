import React, {Component} from 'react';

import {Button, Form, Input, Modal, Select, InputNumber, Switch, Slider} from 'antd';
import countries from 'helpers/static_data/countries'

const FormItem = Form.Item;
const { Option, OptGroup } = Select;



class NewAssistantModal extends Component {

    state = {
        isPopupDisabled: true,
        isAlertsEnabled: false,
        // alertOptions: {0: "Immediately", 4: "4 hours", 8: "8 hours", 12: "12 hours", 24: "24 hours"}
        alertOptions: {0: "Immediately"}
    };

    checkName = (rule, value, callback) => {
        if (!this.props.isAssistantNameValid(value)) {
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

    handleAdd = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                // if(this.state.isPopupDisabled) {values.secondsUntilPopup = 0}
                // values["alertsEnabled"] = this.state.isAlertsEnabled;
                // values.config = {
                //     restrictedCountries: values.restrictedCountries || []
                // };
                // delete values.restrictedCountries;

                this.props.addAssistant(values)
            }
        });
    };



    render() {

        // const alertsKeys = Object.keys(this.state.alertOptions);
        // const maxAlertsLength = parseInt(alertsKeys[alertsKeys.length - 1]);
        // const countriesOptions = [...countries.map(country => <Option key={country.code}>{country.name}</Option>)];

        const {getFieldDecorator} = this.props.form;
        const {hideModal, visible} = this.props;

        return (
            <Modal
                width={500}
                title="Create New Assistant"
                visible={visible}
                onCancel={hideModal}
                destroyOnClose={true}
                footer={[
                    <Button key="cancel" onClick={hideModal}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleAdd}>
                        Add
                    </Button>,
                ]}>
                <Form layout='vertical'>
                    <FormItem
                        label="Assistant Name"
                        extra="Enter a name for your assistant">
                        {getFieldDecorator('assistantName', {
                            rules: [
                                {required: true, message: 'Please input your assistant name'},
                                {validator: this.checkName}
                            ]
                        })(
                            <Input placeholder="Ex: My first assistant, Sales Assistant"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Description"
                        extra="Enter a description for your assistant to easily identify it in the dashboard"
                    >
                        {
                            getFieldDecorator('assistantDesc', {
                                rules: [{
                                    required: false,
                                    message: 'Please input your assistant description'
                                }]
                            })
                            (<Input placeholder="Ex: Qualify candidates for sales job"/>)
                        }
                    </FormItem>

                    <FormItem
                        label="Welcome Message"
                        extra="This will be sent as first message"
                    >
                        {getFieldDecorator('welcomeMessage', {
                            rules: [{
                                required: true, message: 'Please input your welcome message',
                            }],
                        })(
                            <Input placeholder="Ex: Hey there, Welcome visitor"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Header Title"
                        extra="This will appear on top of your chatbot"
                    >
                        {getFieldDecorator('topBarText', {
                            rules: [{
                                required: true,
                                message: 'Please input your header title',
                            }],
                        })(
                            <Input placeholder="Ex: Recruiter Bot"/>
                        )}
                    </FormItem>

                    {/*<FormItem*/}
                    {/*{...formItemLayout}*/}
                    {/*label="Time to Popup"*/}
                    {/*extra="This will enforce the assistants' (chatbot) to popup automatically"*/}
                    {/*>*/}
                    {/*<Switch defaultChecked={false} onChange={this.togglePopupSwitch} style={{marginRight: '5px'}} />*/}
                    {/*{getFieldDecorator('secondsUntilPopup', { initialValue: 1 })(*/}
                        {/*<InputNumber disabled={this.state.isPopupDisabled} min={1} />*/}
                    {/*)}*/}
                    {/*<span className="ant-form-text"> seconds</span>*/}
                    {/*</FormItem>*/}

                    {/*<FormItem*/}
                        {/*{...formItemLayout}*/}
                        {/*label="Restricted Contries"*/}
                        {/*extra="Chatbot will be disabled for users who live in the selected countries"*/}
                    {/*>*/}
                        {/*{*/}
                            {/*getFieldDecorator('restrictedCountries')(*/}
                                {/*<Select mode="multiple" style={{width: '100%'}}*/}
                                        {/*filterOption={(inputValue, option) => option.props.children.toLowerCase().includes(inputValue.toLowerCase())}*/}
                                        {/*placeholder="Please select country or countries">*/}
                                    {/*{countriesOptions}*/}
                                {/*</Select>*/}
                            {/*)*/}
                        {/*}*/}
                    {/*</FormItem>*/}

                    {/*<FormItem*/}
                        {/*{...formItemLayout}*/}
                        {/*label="Record Alert"*/}
                        {/*extra="Turning this on will make the assistant alert you when it has been used"*/}
                    {/*>*/}
                        {/*<Switch checked={this.state.isAlertsEnabled} onChange={this.toggleAlertsSwitch}*/}
                                {/*style={{marginRight: '5px'}}/>*/}
                    {/*</FormItem>*/}

                    {/*<FormItem*/}
                        {/*{...formItemLayout}*/}
                        {/*label="Alerts Every:"*/}
                        {/*extra="Select in what period of time the bot to check for new records and alert you. Note: 'Immediately' could spam your email if your assistant is used a lot"*/}
                    {/*>*/}
                        {/*{getFieldDecorator('alertEvery', {*/}
                            {/*initialValue: parseInt(alertsKeys[alertsKeys.length - 2])*/}
                        {/*})(*/}
                            {/*<Slider*/}
                                {/*max={maxAlertsLength}*/}
                                {/*disabled={!this.state.isAlertsEnabled}*/}
                                {/*marks={this.state.alertOptions} step={null}/>*/}
                        {/*)}*/}
                    {/*</FormItem>*/}

                    {/*<FormItem {...formItemLayout}*/}
                              {/*label="Assistant Templates">*/}

                        {/*{*/}
                            {/*getFieldDecorator('template', {*/}
                                {/*initialValue: 'none',*/}
                                {/*rules: [{*/}
                                    {/*required: true,*/}
                                    {/*message: "Please select a template or None",*/}
                                {/*}]*/}
                            {/*})(*/}
                                {/*<Select>*/}
                                    {/*<Option key={-1} value='none'>None</Option>*/}
                                    {/*{this.props?.options?.assistantTemplates.map((t, i) => {*/}
                                        {/*return (*/}
                                            {/*<OptGroup key={i} label={t.group}>*/}
                                                {/*{t.children.map((c, i) => {*/}
                                                    {/*return (<Option key={i} value={c.fileName}>{c.label}</Option>)*/}
                                                {/*})}*/}
                                            {/*</OptGroup>*/}
                                        {/*)*/}
                                    {/*})}*/}
                                {/*</Select>,*/}
                            {/*)*/}
                        {/*}*/}
                    {/*</FormItem>*/}



                </Form>
            </Modal>
        );
    }
}


export default Form.create()(NewAssistantModal)
