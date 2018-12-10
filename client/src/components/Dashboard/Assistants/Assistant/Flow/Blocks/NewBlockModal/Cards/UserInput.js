import React, {Component} from 'react';
import {Card, Form, Input, Select} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class UserInput extends Component {

    componentWillReceiveProps(nextProps) {
        if (nextProps.beforeAdd)
            this.props.form.validateFields((err, values) => {
                if (!err)
                    this.props.handleNewBlock(values);
                else
                    this.props.handleNewBlock({})
            });
    }

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <Card title="User Input"
                  style={{width: '100%'}}>
                <Form layout='horizontal'>
                    <FormItem label="Question"
                              extra="Enter a name for your assistant to easily identify it in the dashboard"
                              {...this.props.layout}>
                        {getFieldDecorator('text', {
                            rules: [{
                                required: true,
                                message: "Please input your assistant name",
                            }],
                        })(
                            <Input placeholder="Ex: Where are you from?"/>
                        )}
                    </FormItem>

                    <FormItem label="Validation"
                              extra=""
                              {...this.props.layout}>
                        {getFieldDecorator('validation')(
                            <Select placeholder="Will validate the input">
                                <Option value="recruitment">Ignore</Option>
                                <Option value="Shopping">Email</Option>
                                <Option value="Sales">Full Name</Option>
                            </Select>
                        )}
                    </FormItem>

                    <FormItem label="After message"
                              extra=""
                              {...this.props.layout}>
                        {getFieldDecorator('afterMessage')(
                            <Input placeholder="Ex: Your input is considered"/>
                        )}
                    </FormItem>

                </Form>
            </Card>
        );
    }
}

export default Form.create()(UserInput);

