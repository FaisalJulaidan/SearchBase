import React, {Component} from 'react';
import "./NewRequest.less";

import {Form, Input, Select} from 'antd';

const FormItem = Form.Item;
const Option = Select.Option;


class NewRequest extends Component {
    state = {};

    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;

        return (
            <div>
                <Form layout='horizontal'>
                    <FormItem
                        label="Assistant Name"
                        extra="Enter a name for your assistant to easily identify it in the dashboard"
                        {...formItemLayout}>
                        <Input placeholder="Ex: My first assistant, Sales Assistant"/>
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
                        {getFieldDecorator('headerTitle', {
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

                        <Select placeholder="Please select template">
                            <Option value="recruitment">Recruitment</Option>
                            <Option value="Shopping">Shopping</Option>
                            <Option value="Sales">Sales</Option>
                        </Select>
                    </FormItem>

                </Form>
            </div>
        );
    }
}

export default Form.create()(NewRequest)
