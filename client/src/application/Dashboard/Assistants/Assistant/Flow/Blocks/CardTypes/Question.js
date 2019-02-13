import React, {Component} from 'react';
import {Button, Card, Form, Icon, Input, Modal, Popconfirm, Tag, Tooltip} from "antd";

import {getInitialVariables, initActionType} from './CardTypesHelpers'
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    DataTypeFormItem,
    QuestionFormItem,
    ShowGoToBlockFormItem,
    ShowGoToGroupFormItem,
    SkippableFormItem,
    StoreInDBFormItem
} from './CardTypesFormItems'

const FormItem = Form.Item;

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

    //Submit whole block
    onSubmit = () => this.props.form.validateFields(['text', 'isSkippable', 'storeInDB', 'dataType'],
        (err, values) => {
            if (!err) {
                const {flowOptions} = getInitialVariables(this.props.options);
                let options = {
                    block: {
                        Type: 'Question',
                        GroupID: this.props.options.currentGroup.id,
                        StoreInDB: values.storeInDB,
                        Skippable: values.isSkippable || false,
                        DataType: flowOptions.dataTypes.find((dataType) => dataType.name === values.dataType),
                        Content: {
                            text: values.text,
                            answers: this.state.answers
                        }
                    }
                };

                if (this.handleNewBlock)
                    this.handleNewBlock(options);
                else {
                    // Edit Block
                    options.block.ID = this.props.options.block.ID;
                    options.block.Order = this.props.options.block.Order;
                    this.handleEditBlock(options);
                }
            }
    });

    //Add single answer
    addAnswer = () => this.props.form.validateFields(['answer', 'action', 'blockToGoID', 'blockToGoIDGroup', 'afterMessage'],
        (err, values) => {
            if (!err) {
                const answer = {
                    text: values.answer,
                    keywords: this.state.tags,
                    blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                    action: values.action === "Go To Group" ? "Go To Specific Block" : values.action,
                    afterMessage: values.afterMessage
                };
                let answers = [answer].concat(this.state.answers);
                this.setState({answers, tags: []});
                this.hideAddAnswer();
            }
        });
    showAddAnswer = () => this.setState({modalVisible: true});
    hideAddAnswer = () => this.setState({modalVisible: false});
    removeAnswer = deletedAnswer => this.setState({
        answers: [...this.state.answers].filter(answer => (answer.afterMessage !== deletedAnswer.afterMessage) && (answer.text !== deletedAnswer.text))
    });

    //Tags component's functions
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


    componentWillMount() {
        this.handleNewBlock = this.props.handleNewBlock;
        this.handleEditBlock = this.props.handleEditBlock;
        this.handleDeleteBlock = this.props.handleDeleteBlock;

        const {allGroups, block} = getInitialVariables(this.props.options);
        this.setState(initActionType(block, allGroups));
        this.setState({answers: block.Content.answers || []})
    }


    render() {
        const {flowOptions, allGroups, allBlocks, blockOptions, block} = getInitialVariables(this.props.options, 'Question');
        const {getFieldDecorator} = this.props.form;

        const {tags, inputVisible, inputValue} = this.state;

        const buttons = ButtonsForm(this.handleNewBlock, this.handleEditBlock, this.handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{width: '100%'}} actions={buttons}>
                <Form layout='horizontal'>
                    <QuestionFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={this.props.options.layout}
                                      placeholder="Ex: What best describes you?"/>

                    <DataTypeFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator} flowOptions={flowOptions}
                                      layout={this.props.options.layout}/>

                    <FormItem label="Answers"
                              {...this.props.options.layout}>
                        <Button onClick={this.showAddAnswer}
                                type="primary" icon="plus" shape="circle" size={"small"}></Button>
                        {
                            this.state.answers.map((answer, i) => (

                                <Card title={answer.text} key={i}
                                      extra={
                                          <Popconfirm placement="topRight" title="Are you sure delete this answer?"
                                                      onConfirm={() => this.removeAnswer(answer)}
                                                      okText="Yes" cancelText="No">
                                              <Button type="danger" icon="delete" shape="circle"
                                                      size={"small"}></Button>
                                          </Popconfirm>
                                      }
                                      style={{width: 200, margin: 10}}>
                                    <p>Action: {answer.action}</p>
                                    Tags: <br/>
                                    {answer.keywords.map((keyword, i) => <Tag key={i}>{keyword}</Tag>)}
                                </Card>
                            ))
                        }
                    </FormItem>


                    <SkippableFormItem FormItem={FormItem} block={block}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={this.props.options.layout}/>

                    <StoreInDBFormItem FormItem={FormItem} block={block} blockOptions={blockOptions}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={this.props.options.layout}/>

                </Form>


                {/*ADDING ANSWER*/}
                <Modal title="Add Answer" width={700} destroyOnClose={true} visible={this.state.modalVisible}
                       onOk={this.addAnswer} onCancel={this.hideAddAnswer}>
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

                        <FormItem label="Keywords" {...this.props.options.layout}>
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

                        <ActionFormItem FormItem={FormItem} blockOptions={blockOptions} block={block}
                                        setStateHandler={(state) => this.setState(state)}
                                        getFieldDecorator={getFieldDecorator}
                                        layout={this.props.options.layout}/>

                        <ShowGoToBlockFormItem FormItem={FormItem} allBlocks={allBlocks} block={block}
                                               showGoToBlock={this.state.showGoToBlock}
                                               getFieldDecorator={getFieldDecorator}
                                               layout={this.props.options.layout}/>

                        <ShowGoToGroupFormItem FormItem={FormItem} allGroups={allGroups}
                                               showGoToGroup={this.state.showGoToGroup}
                                               getFieldDecorator={getFieldDecorator}
                                               layout={this.props.options.layout}/>

                        <AfterMessageFormItem FormItem={FormItem} block={block}
                                              getFieldDecorator={getFieldDecorator}
                                              layout={this.props.options.layout}/>
                    </Form>

                </Modal>
            </Card>
        );
    }

}


export default Form.create()(Question);

