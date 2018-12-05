import React, {Component} from 'react';
import "./EditAssistant.less"
import styles from "./EditAssistant.module.less"
import {Button, Form, Input, InputNumber, Slider} from "antd";
import {authActions} from "../../../store/actions";

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

    componentWillUnmount = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                this.props.assistantCallback(values);
            }
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

        return (
            <Form layout='horizontal'>
                <FormItem
                    label="Assistant Name"
                    extra="Enter a name for your assistant to easily identify it in the dashboard"
                    {...formItemLayout}>
                    {
                        getFieldDecorator('Name', {
                            initialValue: assistant.Name,
                            rules: [{
                                required: true,
                                message: 'Please input your assistant name',
                            }],
                        })
                        (<Input placeholder="Ex: My first assistant, Sales Assistant"/>)
                    }

                    <Button onClick={this.submit}/>
                </FormItem>

                <FormItem
                    label="Welcome Message"
                    extra="This will be sent as first message"
                    {...formItemLayout}>
                    {getFieldDecorator('Message', {
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
                    {
                        getFieldDecorator('TopBarText', {
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

                <FormItem {...formItemLayout}
                          label="Assistant Template">
                    <Slider min={0} max={100}
                            onChange={this.onChange}
                            value={typeof inputValue === 'number' ? inputValue : 0}
                    />
                    {
                        getFieldDecorator('SecondsUntilPopup', {
                            initialValue: inputValue,
                            rules: [{
                                required: true,
                                message: 'Please input your header title',
                            }],
                        })(
                            <InputNumber min={0} max={100}
                                         onChange={this.onChange}
                            />
                        )
                    }
                </FormItem>

            </Form>
        );
    }
}

export default Form.create()(EditAssistant)
