import React, {Component} from 'react';
import {Button, Card, Checkbox, Form, Input, Select, Spin} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class UserInput extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
        groupName: ''
    };


    componentWillMount() {
        this.handleNewBlock = this.props.handleNewBlock;
        this.handleEditBlock = this.props.handleEditBlock
    }

    onSubmit = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            let options = {
                block: {
                    type: 'User Input',
                    groupID: this.props.options.currentGroup.id,
                    storeInDB: values.storeInDB,
                    isSkippable: values.isSkippable || false,
                    dataCategoryID: values.dataCategoryID,
                    content: {
                        text: values.text,
                        blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                        validation: values.validation,
                        action: values.action,
                        afterMessage: values.afterMessage
                    }
                }
            };

            if (this.handleNewBlock)
                this.handleNewBlock(options);
            else {
                // Edit Block
                options.block.id = this.props.options.block.id;
                options.block.order = this.props.options.block.order;
                this.handleEditBlock(options);
            }

        }
    });


    onDelete = () => this.props.handleDeleteBlock({
        id: this.props.options.block.id,
        type: 'User Input',
    });

    onCancel = () => this.handleNewBlock ? this.handleNewBlock(false) : this.handleEditBlock(false);

    onSelectAction = (action) => {
        if (action === "Go To Specific Block")
            this.setState({showGoToBlock: true, showGoToGroup: false});
        else if (action === "Go To Group")
            this.setState({showGoToBlock: false, showGoToGroup: true});
        else
            this.setState({showGoToBlock: false, showGoToGroup: false});
    };

    componentDidMount() {
        const {allGroups} = this.props.options;
        let block = this.props.options.block ? this.props.options.block : {content: {}};
        if (block.content.action === "Go To Specific Block")
            this.setState({showGoToBlock: true, showGoToGroup: false});
        else if (block.content.action === "Go To Group") {
            // because here we dont' have column in each block contains all the group
            // this is a workaround to have the group name from the block id
            this.setState({showGoToBlock: false, showGoToGroup: true});
            const {blockToGoID} = block.content;
            allGroups.map((group) => group.blocks[0].id === blockToGoID ? this.setState({groupName: group.name}) : null)
        } else
            this.setState({showGoToBlock: false, showGoToGroup: false});
    }

    render() {
        const {flowOptions, allGroups, allBlocks} = this.props.options;
        let blockOptions = {};
        let block = this.props.options.block ? this.props.options.block : {content: {}};

        // extract the correct blockType from blockTypes[]
        for (const blockType of flowOptions.blockTypes)
            if (blockType.name === 'User Input')
                blockOptions = blockType;

        const {getFieldDecorator} = this.props.form;

        const buttons = this.handleNewBlock ? [
            <Button key="cancel" onClick={this.onCancel}>Cancel</Button>,
            <Button key="submit" type="primary" onClick={this.onSubmit}>Add</Button>
        ] : [
            <Button key="delete" type="danger" onClick={this.onDelete}>
                Delete
            </Button>,
            <Button key="cancel" onClick={this.onCancel}>Cancel</Button>,
            <Button key="submit" type="primary" onClick={this.onSubmit}>Update</Button>
        ];


        return (
            <Card style={{width: '100%'}} actions={buttons}>
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
                            <Input placeholder="Ex: Where are you from?"/>
                        )}
                    </FormItem>

                    <FormItem label="Data Category"
                              extra="Categorising users' responses will result in  more efficient AI processing"
                              {...this.props.options.layout}>
                        {
                            getFieldDecorator('dataCategoryID', {
                                initialValue: null,
                                rules: [{
                                    required: true,
                                    message: "Please specify the data category",
                                }]
                            })(
                                <Select placeholder="Will validate the input">
                                    {
                                        flowOptions.dataCategories.map((category, i) =>
                                            <Option key={i} value={category.ID}>{category.Name}</Option>)
                                    }
                                </Select>
                            )
                        }
                    </FormItem>

                    <FormItem label="Validation"
                              {...this.props.options.layout}>
                        {
                            blockOptions.validations ?
                                getFieldDecorator('validation', {
                                    initialValue: block.content.validation,
                                    rules: [{
                                        required: true,
                                        message: "Please select a validation type",
                                    }]
                                })(
                                    <Select placeholder="Will validate the input">
                                        {
                                            blockOptions.validations.map((validation, i) =>
                                                <Option key={i} value={validation}>{validation}</Option>)
                                        }
                                    </Select>
                                )
                                : <Spin><Select placeholder="Will validate the input"></Select></Spin>
                        }
                    </FormItem>

                    <FormItem label="Action"
                              {...this.props.options.layout}>
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

export default Form.create()(UserInput);