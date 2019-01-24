import React, {Component} from 'react';
import {Button, Card, Checkbox, Form, Icon, Input, Modal, Select, Spin, Tag, Tooltip} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class Question extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
        modalVisible: false,

        tags: [],
        inputVisible: false,
        inputValue: '',
        answers: [],

        groupName: ''
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

        this.setState({answers: block.content.answers || []})
    }

    componentWillMount() {
        this.handleNewBlock = this.props.handleNewBlock;
        this.handleEditBlock = this.props.handleEditBlock
    }

    onSelectAction = (action) => {
        if (action === "Go To Specific Block")
            this.setState({showGoToBlock: true, showGoToGroup: false});
        else if (action === "Go To Group")
            this.setState({showGoToBlock: false, showGoToGroup: true});
        else
            this.setState({showGoToBlock: false, showGoToGroup: false});
    };

    onSubmit = () => this.props.form.validateFields(['text', 'isSkippable', 'storeInDB', 'dataCategoryID'], (err, values) => {
        if (!err) {
            let options = {
                block: {
                    type: 'Question',
                    groupID: this.props.options.currentGroup.id,
                    storeInDB: values.storeInDB,
                    isSkippable: values.isSkippable || false,
                    dataCategoryID: values.dataCategoryID,
                    content: {
                        text: values.text,
                        answers: this.state.answers
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

    onDeleteBlock = () => this.props.handleDeleteBlock({
        id: this.props.options.block.id,
        type: 'Question',
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

    addAnswer = () => {
        this.props.form.validateFields(['answer', 'action', 'blockToGoID', 'blockToGoIDGroup', 'afterMessage'], (err, values) => {
            if (!err) {
                const answer = {
                    text: values.answer,
                    keywords: this.state.tags,
                    blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                    action: values.action === "Go To Group" ? "Go To Specific Block" : values.action,
                    afterMessage: values.afterMessage
                };
                this.setState({tags: []});
                const answers = this.state.answers;
                answers.push(answer);
                this.setState({answers});
                this.hideAddAnswer();
                console.log(this.state.answers)
            }
        })

    };

    showAddAnswer = () => this.setState({modalVisible: true});
    hideAddAnswer = () => this.setState({modalVisible: false});

    removeAnswer = deletedAnswer => this.setState({
        answers: [...this.state.answers].filter(answer =>
            (answer.afterMessage !== deletedAnswer.afterMessage) &&
            (answer.text !== deletedAnswer.text))
    });

// Tags component's functions
    removeTag = (removedTag) => this.setState({tags: this.state.tags.filter(tag => tag !== removedTag)});
    showInput = () => this.setState({inputVisible: true}, () => this.input.focus());
    handleInputChange = e => this.setState({inputValue: e.target.value});
    saveInputRef = input => this.input = input;
    handleInputConfirm = () => {
        const inputValue = this.state.inputValue;
        let tags = this.state.tags;
        if (inputValue && tags.indexOf(inputValue) === -1)
            tags = [...tags, inputValue];
        this.setState({tags, inputVisible: false, inputValue: '',});
    };

// END Tags component's functions


    render() {
        const {flowOptions, allGroups, allBlocks} = this.props.options;
        let blockOptions = {};
        let block = this.props.options.block ? this.props.options.block : {content: {}};

        // extract the correct blockType from blockTypes[]
        for (const blockType of flowOptions.blockTypes)
            if (blockType.name === 'Question')
                blockOptions = blockType;

        const {getFieldDecorator} = this.props.form;

        const {tags, inputVisible, inputValue} = this.state;

        const buttons = this.handleNewBlock ? [
            <Button key="cancel" onClick={this.onCancel}>Cancel</Button>,
            <Button key="submit" type="primary" onClick={this.onSubmit}>Add</Button>
        ] : [
            <Button key="delete" type="danger" onClick={this.onDeleteBlock}>Delete</Button>,
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
                                initialValue: null || block.dataCategoryID,
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

                    <FormItem label="Answers"
                              {...this.props.options.layout}>
                        <Button onClick={this.showAddAnswer}
                                type="primary" icon="plus" shape="circle" size={"small"}></Button>
                        {
                            this.state.answers.map((answer, i) => (
                                <Card title={answer.text}
                                      key={i}
                                      extra={<Button onClick={() => this.removeAnswer(answer)}
                                                     type="danger" icon="delete" shape="circle"
                                                     size={"small"}></Button>}
                                      style={{width: 200, margin: 10}}>
                                    <p>Action: {answer.action}</p>
                                    Tags: <br/>
                                    {answer.keywords.map((keyword, i) => <Tag key={i}>{keyword}</Tag>)}
                                </Card>
                            ))
                        }
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


                {/*ADDING ANSWER*/}
                <Modal
                    title="Add Answer"
                    width={700}
                    destroyOnClose={true}
                    visible={this.state.modalVisible}
                    onOk={this.addAnswer}
                    onCancel={this.hideAddAnswer}>

                    <Form>
                        <FormItem label="Answer"
                                  extra="This will be shown as answer in chatbot"
                                  {...this.props.options.layout}>
                            {getFieldDecorator('answer', {
                                rules: [{
                                    required: true,
                                    message: "Please input answer field",
                                }],
                            })(
                                <Input placeholder="Ex: Yes I need it :)"/>
                            )}
                        </FormItem>

                        <FormItem label="Tags" {...this.props.options.layout}>
                            <div>
                                {tags.map((tag) => {
                                    const isLongTag = tag.length > 20;
                                    const tagElem = (
                                        <Tag key={tag} closable={true} afterClose={() => this.removeTag(tag)}>
                                            {isLongTag ? `${tag.slice(0, 20)}...` : tag}
                                        </Tag>
                                    );
                                    return isLongTag ? <Tooltip title={tag} key={tag}>{tagElem}</Tooltip> : tagElem;
                                })}
                                {inputVisible && (
                                    <Input
                                        ref={this.saveInputRef}
                                        type="text"
                                        size="small"
                                        style={{width: 78}}
                                        value={inputValue}
                                        onChange={this.handleInputChange}
                                        onBlur={this.handleInputConfirm}
                                        onPressEnter={this.handleInputConfirm}
                                    />
                                )}
                                {!inputVisible && (
                                    <Tag
                                        onClick={this.showInput}
                                        style={{background: '#fff', borderStyle: 'dashed'}}>
                                        <Icon type="plus"/> New Tag
                                    </Tag>
                                )}
                            </div>
                        </FormItem>

                        <FormItem label="Action"{...this.props.options.layout}>{
                            blockOptions.actions ?
                                getFieldDecorator('action', {
                                    rules: [{
                                        required: true,
                                        message: "Please input action field",
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
                        }</FormItem>

                        {this.state.showGoToBlock ?
                            (<FormItem label="Go To Specific Block" {...this.props.options.layout}>
                                {
                                    getFieldDecorator('blockToGoID',
                                        {
                                            rules: [{required: true, message: "Please select your next block"}],
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
                                <Input placeholder="Ex: Your input is recorded"/>
                            )}
                        </FormItem>
                    </Form>

                </Modal>
            </Card>
        );
    }

}


export default Form.create()(Question);

