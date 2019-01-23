import React, {Component} from 'react';
import {Button, Card, Checkbox, Form, Input, Select, Spin} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class Solutions extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false
    };

    onSubmit = () => {
        return this.props.form.validateFields((err, values) => {
            // If from is valid crete the new block following User Input block type format
            if (!err) {
                const newBlock = {
                    block: {
                        type: 'Solutions',
                        groupID: this.props.options.currentGroup.id,
                        storeInDB: false,
                        isSkippable: false,
                        dataCategoryID: null,
                        content: {
                            showTop: Number(values.showTop),
                            action: values.action,
                            blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                            afterMessage: values.afterMessage,
                        }
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

    render() {
        const {flowOptions, blocks, allGroups} = this.props.options;
        let blockOptions = {};
        // extract the correct blockType from blockTypes[]
        for (const blockType of flowOptions.blockTypes)
            if (blockType.name === 'User Input')
                blockOptions = blockType;

        const {getFieldDecorator} = this.props.form;
        return (
            <Card style={{width: '100%'}}
                  actions={[
                      <Button key="cancel" onClick={this.onCancel}>Cancel</Button>,
                      <Button key="submit" type="primary" onClick={this.onSubmit}>Add</Button>]}
            >
                <Form layout='horizontal'>
                    <FormItem label="Show Top Results"
                              extra="Number of results you want to return (Best matches)"
                              {...this.props.options.layout}>
                        {getFieldDecorator('showTop', {
                            rules: [{
                                required: true,
                                message: "Please set how many solutions to return",
                            }],
                        })(
                            <Input min="1" type="number" placeholder="Ex: 5"/>
                        )}
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
                                        rules: [{required: true, message: "Please select your next block"}]

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
                                getFieldDecorator('blockToGoIDGroup',
                                    {
                                        rules: [{required: true, message: "Please select your next group"}]
                                    }
                                )(
                                    <Select placeholder="The next block after this block">{
                                        allGroups.map((group, i) => {
                                                if (group.blocks[0])
                                                    return <Option key={i} value={group.blocks[0].id}>
                                                        {`${group.name}`}
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
                                message: "Please input after message field",
                            }],
                        })(
                            <Input placeholder="Ex: There you go :)"/>
                        )}
                    </FormItem>
                </Form>
            </Card>
        );
    }
}

export default Form.create()(Solutions);

