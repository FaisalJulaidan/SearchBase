import React, {Component} from 'react';
import {Button, Card, Checkbox, Form, Input, Select, Spin} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;
const CheckboxGroup = Checkbox.Group;

class FileUpload extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
        fileTypes: [],
        groupName: ''
    };

    onSubmit = () => {
        return this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.handleEditBlock({
                    type: 'File Upload',
                    groupID: this.props.options.currentGroup.id,
                    storeInDB: values.storeInDB,
                    isSkippable: values.isSkippable,
                    labels: '',
                    content: {
                        text: values.text,
                        action: values.action,
                        fileTypes: this.state.fileTypes,
                        blockToGoID: values.blockToGoID || values.blockToGoIDGroup,
                        afterMessage: values.afterMessage
                    }
                })
            }
        })
    };

    onCancel = () => this.props.handleEditBlock(false);

    onSelectAction = (action) => {
        if (action === "Go To Specific Block")
            this.setState({showGoToBlock: true, showGoToGroup: false});
        else if (action === "Go To Group")
            this.setState({showGoToBlock: false, showGoToGroup: true});
        else
            this.setState({showGoToBlock: false, showGoToGroup: false});
    };

    componentDidMount() {
        const {block, allGroups} = this.props.options;

        if (block.content.action === "Go To Specific Block")
            this.setState({showGoToBlock: true, showGoToGroup: false});
        else if (block.content.action === "Go To Group") {
            // because here we dont' have column in each block contains all the group
            // this is a workaround to have the group name from the block id
            this.setState({showGoToBlock: false, showGoToGroup: true});
            const {blockToGoID} = block.content;
            allGroups.map((group) => group.blocks[0].id === blockToGoID ? this.setState({groupName: group.name}) : null)
        }
        else
            this.setState({showGoToBlock: false, showGoToGroup: false});
    }

    onChange = (checkedValues) => this.setState({fileTypes: checkedValues});

    render() {
        const {block, blockTypes, allBlocks, allGroups} = this.props.options;
        let blockOptions = {};
        // extract the correct blockType from blockTypes[]

        for (const blockType of blockTypes)
            if (blockType.name === "File Upload")
                blockOptions = blockType;
        const {getFieldDecorator} = this.props.form;

        const typesAllowed = blockOptions.typesAllowed;
        return (
            <Card style={{width: '100%'}}
                  actions={[
                      <Button key="delete" type="danger" onClick={() => console.log('needs to be implement')}>
                          Delete
                      </Button>,
                      <Button key="cancel" onClick={() => this.props.handleEditBlock(false)}>Cancel</Button>,
                      <Button key="submit" type="primary" onClick={this.onSubmit}>
                          Update
                      </Button>]}
            >
                <Form layout='horizontal'>
                    <FormItem label="Question"
                              extra="The above text will be shown in a bubble inside the chat"
                              {...this.props.options.layout}>
                        {getFieldDecorator('text', {
                            initialValue: block.content.text,
                            rules: [{
                                required: true,
                                message: "Please input question field",
                            }],
                        })(
                            <Input placeholder="Ex: Please upload you cv"/>
                        )}
                    </FormItem>

                    <FormItem label="File Types"
                              {...this.props.options.layout}>
                        {
                            blockOptions.typesAllowed ?
                                getFieldDecorator('fileTypes', {
                                    initialValue: block.content.fileTypes,
                                    rules: [{
                                        required: true,
                                        message: "Please select the accepted file type",
                                    }]
                                })(
                                    <CheckboxGroup options={typesAllowed} onChange={this.onChange}/>
                                )
                                : <Spin/>
                        }
                    </FormItem>

                    <FormItem label="Action"{...this.props.options.layout}>
                        {
                            blockOptions.actions ?
                                getFieldDecorator('action', {
                                    initialValue: block.content.action,
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
                                        initialValue: block.content.blockToGoID,
                                        rules: [{required: true, message: "Please select your next block"}]

                                    }
                                )(
                                    <Select placeholder="The next step after this block">{
                                        allBlocks.map((block, i) =>
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
                                        initialValue: this.state.groupName,
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
                            initialValue: block.content.afterMessage,
                            rules: [{
                                required: true,
                                message: "Please input after message field",
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
                            initialValue: block.isSkippable,
                        })(
                            <Checkbox>Users can skip answering this question</Checkbox>
                        )}
                    </Form.Item>

                    <Form.Item
                        label="Store responses?"
                        {...this.props.options.layout}>
                        {getFieldDecorator('storeInDB', {
                            valuePropName: 'checked',
                            initialValue: blockOptions.alwaysStoreInDB,
                        })(
                            <Checkbox disabled={blockOptions.alwaysStoreInDB}>
                                Users' responses should be recorded</Checkbox>
                        )}
                    </Form.Item>

                </Form>
            </Card>
        );
    }
}

export default Form.create()(FileUpload);

