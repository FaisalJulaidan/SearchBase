import React, {Component} from 'react';
import {Card, Form, Input, Select, Spin} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class UserInput extends Component {

    componentWillReceiveProps(nextProps) {
        if (nextProps.beforeAdd)
            this.props.form.validateFields((err, values) => {
                if (!err)
                    this.props.handleNewBlock(values);
                else
                    this.props.handleNewBlock(false);
            });
    }

    render() {
        const {blockTypes} = this.props.options;

        let blockOptions = {};
        // extract the correct blockType from blockTypes[]
        for (const blockType of blockTypes)
            if (blockType.name === 'User Input')
                blockOptions = blockType;

        const {getFieldDecorator} = this.props.form;
        return (
            <Card title="User Input"
                  style={{width: '100%'}}>

                <Form layout='horizontal'>
                    <FormItem label="Question"
                              extra="The above text will be shown in a bubble inside the chat"
                              {...this.props.options.layout}>
                        {getFieldDecorator('text', {
                            rules: [{
                                required: true,
                                message: "Please input question field",
                            }],
                        })(
                            <Input placeholder="Ex: Where are you from?"/>
                        )}
                    </FormItem>

                    <FormItem label="Validation"
                              {...this.props.options.layout}>
                        {
                            blockOptions.validations ?
                                getFieldDecorator('validation')(
                                    <Select placeholder="Will validate the input">{
                                        blockOptions.validations.map((validation, i) =>
                                            <Option key={i} value={validation}>{validation}</Option>)
                                    }</Select>
                                )
                                : <Spin><Select placeholder="Will validate the input"></Select></Spin>
                        }
                    </FormItem>

                    <FormItem label="Action"
                              {...this.props.options.layout}>
                        {
                            blockOptions.actions ?
                                getFieldDecorator('action', {
                                    rules: [{
                                        required: true,
                                        message: "Please input question field",
                                    }],
                                })(
                                    <Select placeholder="The next step after this block">{
                                        blockOptions.actions.map((action, i) =>
                                            <Option key={i} value={action}>{action}</Option>)
                                    }</Select>
                                )
                                : <Spin><Select placeholder="The next step after this block"></Select></Spin>
                        }
                    </FormItem>

                    <FormItem label="After message"
                              extra=""
                              {...this.props.options.layout}>
                        {getFieldDecorator('afterMessage', {
                            rules: [{
                                required: true,
                                message: "Please input question field",
                            }],
                        })(
                            <Input placeholder="Ex: Your input is recorded"/>
                        )}
                    </FormItem>

                </Form>
            </Card>
        );
    }
}

export default Form.create()(UserInput);

