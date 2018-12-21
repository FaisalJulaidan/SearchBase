import React, {Component} from 'react';
import {Button, Card, Checkbox, Form, Input, Select, Spin, Tag, Modal, Icon, Tooltip} from "antd";

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
        answers: []
    };

    onSubmit = () => {
        return this.props.form.validateFields(['text', 'isSkippable', 'storeInDB'], (err, values) => {

            // add answers from state to the object then do the schema and send to serever


            // If from is valid crete the new block following User Input block type format
            if (!err) {
                const newBlock = {
                    type: 'Question',
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


    addAnswer = () => {
        this.props.form.validateFields(['answer', 'action', 'blockToGoID', 'blockToGoID', 'afterMessage'], (err, values) => {
            if (!err) {
                const answer = {
                    ...values,
                    keywords: this.state.tags
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
    removeAnswer = () => {
        console.log("TODO")
    };

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
        const {blockTypes, blocks, allGroups} = this.props.options;
        let blockOptions = {};
        // extract the correct blockType from blockTypes[]
        for (const blockType of blockTypes)
            if (blockType.name === 'User Input')
                blockOptions = blockType;

        const {getFieldDecorator} = this.props.form;

        const {tags, inputVisible, inputValue} = this.state;

        return (
            <Card title="Question"
                  style={{width: '100%'}}
                  actions={[
                      <Button key="cancel" onClick={this.onCancel}>Cancel</Button>,
                      <Button key="submit" type="primary" onClick={this.onSubmit}>Add</Button>]}>
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
                        <Button onClick={this.showAddAnswer}
                                type="primary" icon="plus" shape="circle" size={"small"}></Button>
                        {
                            this.state.answers.map((answer, i) => (
                                <Card title={answer.answer}
                                      key={i}
                                      extra={<Button onClick={this.removeAnswer}
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

