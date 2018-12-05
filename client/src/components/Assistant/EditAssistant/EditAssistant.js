import React, {Component} from 'react';
import "./EditAssistant.less"
import styles from "./EditAssistant.module.less"
import {Form, Input, InputNumber, Slider} from "antd";

const FormItem = Form.Item;


class EditAssistant extends Component {
    state = {
        inputValue: 10,
    };

    onChange = (value) => {
        this.setState({
            inputValue: value,
        });
    };

    componentDidMount() {
        this.setState({
            inputValue: this.props.assistant.SecondsUntilPopup
        });
    }

    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;
        const {assistant} = this.props;


        const {inputValue} = this.state;


        console.log(assistant)
        const x = {
            Message: "Hey there",
            Name: "Helper",
            SecondsUntilPopup: 1,
            TopBarText: "Aramco Bot"
        }
        return (
            <Form layout='horizontal'>
                <FormItem
                    label="Assistant Name"
                    extra="Enter a name for your assistant to easily identify it in the dashboard"
                    {...formItemLayout}>
                    <Input placeholder="Ex: My first assistant, Sales Assistant" defaultValue={assistant.Name}/>
                </FormItem>


                <FormItem
                    label="Welcome Message"
                    extra="This will be sent as first message"
                    {...formItemLayout}>
                    {getFieldDecorator('welcomeMessage', {
                        initialValue: assistant.Message,
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
                    {getFieldDecorator('headerTitle', {
                        initialValue: assistant.TopBarText,
                        rules: [{
                            required: true,
                            message: 'Please input your header title',
                        }],
                    })(
                        <Input placeholder="Ex: Recruiter Bot"/>
                    )}
                </FormItem>

                <FormItem {...formItemLayout}
                          label="Assistant Template">

                    <Slider min={0} max={100}
                            onChange={this.onChange}
                            value={typeof inputValue === 'number' ? inputValue : 0}
                    />
                    <InputNumber min={0} max={100}
                                 value={inputValue}
                                 onChange={this.onChange}
                    />
                </FormItem>

            </Form>
        );
    }
}

export default Form.create()(EditAssistant)
