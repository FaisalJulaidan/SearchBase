import React, {Component} from 'react';
import {Card, Form, Input, Select, Spin} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class FileUpload extends Component {

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
        const {blockTypes} = this.props.options;

        let blockOptions = {};
        // extract the correct blockType from blockTypes[]
        for (const blockType of blockTypes)
            if (blockType.name === 'File Upload')
                blockOptions = blockType;

        const {getFieldDecorator} = this.props.form;
        return (
            <Card title="File Upload"
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

                    <FormItem label="Action"
                              {...this.props.options.layout}>
                        {
                            blockOptions.actions ?
                                getFieldDecorator('action')(
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
                        {getFieldDecorator('afterMessage')(
                            <Input placeholder="Ex: Your input is recorded"/>
                        )}
                    </FormItem>

                </Form>
            </Card>
        );
    }
}

export default Form.create()(FileUpload);
