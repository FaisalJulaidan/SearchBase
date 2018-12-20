import React, {Component} from 'react';
import {Button, Card, Checkbox, Form, Input, Select, Spin, Tag, Modal} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class Question extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
        modalVisible: false
    };

    onSubmit = () => {
        return this.props.form.validateFields((err, values) => {
            // If from is valid crete the new block following User Input block type format
            if (!err) {
                const newBlock = {
                    type: 'User Input',
                    groupID: this.props.options.currentGroup.id,
                    storeInDB: values.storeInDB,
                    isSkippable: values.isSkippable,
                    labels: '',
                    content: {
                        text: values.text,
                        blockToGoID: values.blockToGoID,
                        validation: values.validation,
                        action: values.action,
                        afterMessage: values.afterMessage
                    }
                };
                this.props.handleNewBlock(newBlock)
            }
        })
    };

    onCancel = () => this.props.handleNewBlock(false);

    onSelectAction = (action) => {
        if (action === "Go To Specific Block")
            this.setState({showGoToBlock: true, showGoToGroup: false});
        else if (action === "Go To Group")
            this.setState({showGoToBlock: false, showGoToGroup: true});
        else
            this.setState({showGoToBlock: false, showGoToGroup: false});
    };

    addAnswer = () => this.setState({modalVisible: true});

    handleCancel = () => this.setState({modalVisible: false});


    render() {
        const {blockTypes, blocks, allGroups} = this.props.options;
        let blockOptions = {};
        // extract the correct blockType from blockTypes[]
        for (const blockType of blockTypes)
            if (blockType.name === 'User Input')
                blockOptions = blockType;

        const {getFieldDecorator} = this.props.form;

        const answer = (
            <Card
                title="Answer"
                extra={<a href="#">Edit</a>}
                style={{width: 200, margin: 10}}>
                <p>Action: go to next step</p>
                Tags: <br/>
                <Tag><a>Link</a></Tag>
                <Tag><a>Link</a></Tag>
                <Tag><a>Link</a></Tag>
                <Tag><a>Link</a></Tag>
                <Tag><a>Link</a></Tag>

            </Card>
        );
        return (
            <Card title="User Input"
                  style={{width: '100%'}}
                  actions={[
                      <Button key="cancel" onClick={this.onCancel}>Cancel</Button>,
                      <Button key="submit" type="primary" onClick={this.onSubmit}>Add</Button>]}
            >
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

                    <FormItem label="Answers"
                              {...this.props.options.layout}>
                        <Button onClick={this.addAnswer}
                                type="primary" icon="plus" shape="circle" size={"small"}></Button>
                        {answer}{answer}{answer}{answer}{answer}{answer}
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
                                    <Select onSelect={this.onSelectAction}
                                            placeholder="The next step after this block">{
                                        blockOptions.actions.map((action, i) =>
                                            <Option key={i}
                                                    value={action}>{action}</Option>)
                                    }</Select>
                                )
                                : <Spin><Select placeholder="The next step after this block"></Select></Spin>
                        }
                    </FormItem>

                    {this.state.showGoToBlock ?
                        (<FormItem label="Go To Specific Block" {...this.props.options.layout}>
                            {
                                getFieldDecorator('blockToGoID',
                                    {
                                        rules: [{required: true, message: "Please select your next block"}],
                                        initialValue: null

                                    }
                                )(
                                    <Select placeholder="The next step after this block">{
                                        blocks.map((block, i) =>
                                            <Option key={i} value={block.id}>
                                                {`${block.id}- (${block.type}) ${block.content.text ? block.content.text : ''}`}
                                            </Option>
                                        )
                                    }</Select>
                                )
                            }
                        </FormItem>)
                        : null
                    }

                    {this.state.showGoToGroup ?
                        (<FormItem label="Go To Specific Group"
                                   extra="The selected group will start from its first block"
                                   {...this.props.options.layout}>
                            {
                                getFieldDecorator('blockToGoID',
                                    {
                                        rules: [{required: true, message: "Please select your next group"}]
                                    }
                                )(
                                    <Select placeholder="The next block after this block">{
                                        allGroups.map((group, i) => {
                                                if (group.blocks[0])
                                                    return <Option key={i} value={group.blocks[0].id}>
                                                        {`${group.name}`}d
                                                    </Option>;
                                                else
                                                    return <Option disabled key={i} value={group.name}>
                                                        {`${group.name}`}
                                                    </Option>
                                            }
                                        )
                                    }</Select>
                                )
                            }
                        </FormItem>)
                        : null
                    }

                    <FormItem label="After message"
                              extra="This message will display straight after the user's response"
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

                    <Form.Item
                        label="Skippable?"
                        {...this.props.options.layout}>
                        {getFieldDecorator('isSkippable', {
                            valuePropName: 'checked',
                            initialValue: false,
                        })(
                            <Checkbox>Users can skip answering this question"</Checkbox>
                        )}
                    </Form.Item>

                    <Form.Item
                        label="Store responses?"
                        {...this.props.options.layout}>
                        {getFieldDecorator('storeInDB', {
                            valuePropName: 'checked',
                            initialValue: true,
                        })(
                            <Checkbox>Users' responses should be recorded</Checkbox>
                        )}
                    </Form.Item>

                </Form>

                <Modal
                    title="Add Answer"
                    visible={this.state.modalVisible}
                    onOk={this.addAnswer}
                    onCancel={this.handleCancel}>
                    <p>Some contents...</p>
                    <p>Some contents...</p>
                    <p>Some contents...</p>
                </Modal>
            </Card>
        );
    }

}

export default Form.create()(Question);

