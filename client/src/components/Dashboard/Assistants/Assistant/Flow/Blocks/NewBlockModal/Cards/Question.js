import React, {Component} from 'react';
import {Card, Form, Input, Select} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class Question extends Component {

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
        return (<Card title="Question"
                      style={{width: '100%'}}>

                <Form layout='horizontal'>

                    <FormItem
                        label="Assistant Name"
                        extra="Enter a name for your assistant to easily identify it in the dashboard"
                        {...this.props.layout}>
                        {getFieldDecorator('testField', {
                            rules: [{
                                required: true,
                                message: 'Please input your assistant name',
                            }],
                        })(
                            <Input placeholder="Ex: My first assistant, Sales Assistant"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Question"
                        {...this.props.layout}>
                        <Input placeholder="Ex: Where are you from?"/>
                    </FormItem>

                    <FormItem {...this.props.layout}
                              label="Validation">

                        <Select placeholder="Will validate the input">
                            <Option value="recruitment">Ignore</Option>
                            <Option value="Shopping">Email</Option>
                            <Option value="Sales">Full Name</Option>
                        </Select>
                    </FormItem>

                    <FormItem
                        label="After message"
                        {...this.props.layout}>
                        <Input placeholder="Ex: Your input is considered"/>
                    </FormItem>

                </Form>
            </Card>
        );
    }

}

export default Form.create()(Question);

