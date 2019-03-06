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
    onSubmit = (formBlock) => this.props.form.validateFields(['text', 'isSkippable', 'storeInDB', 'dataType'],
        (err, values) => {
            if (!err) {
                const flowOptions = this.props.options.flow;
                let options = {
                    Type: 'Question',
                    StoreInDB: values.storeInDB,
                    Skippable: values.isSkippable || false,
                    DataType: flowOptions.dataTypes.find((dataType) => dataType.name === values.dataType),
                    Content: {
                        text: values.text,
                        answers: this.state.answers
                    }
                };

                if (this.props.handleNewBlock)
                    this.props.handleNewBlock(options);
                else {
                    // Edit Block
                    options.ID = this.props.modalState.block.ID;
                    this.props.handleEditBlock(options);
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
                    afterMessage: values.afterMessage || "",
                    ID: values.answer + "%" + Date.now()
                };
                let answers = [answer].concat(this.state.answers);
                this.setState({answers, tags: []});
                this.hideAddAnswer();
            }
        });
    showAddAnswer = () => this.setState({modalVisible: true});
    hideAddAnswer = () => this.setState({modalVisible: false});
    removeAnswer = deletedAnswer => this.setState({
        answers: [...this.state.answers].filter(answer => answer.ID !== deletedAnswer.ID)
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
        const {modalState, options} = this.props;
        const {block} = getInitialVariables(options.flow, modalState);
        this.setState(initActionType(block, this.props.modalState.allGroups));
        this.setState({answers: block.Content.answers || []})
    }


    render() {
        const {modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock} = this.props;
        const {blockOptions, block} = getInitialVariables(options.flow ,modalState, 'Question');
        const {allGroups, allBlocks, currentGroup, layout} = modalState;
        const {getFieldDecorator} = form;

        const {tags, inputVisible, inputValue} = this.state;

        const buttons = ButtonsForm(handleNewBlock, handleEditBlock, handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{width: '100%'}} actions={buttons}>
                <Form layout='horizontal'>
                    <QuestionFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={layout}
                                      placeholder="Ex: What best describes you?"/>

                    <DataTypeFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      options={this.props.options}
                                      layout={layout}/>

                    <FormItem label="Answers"
                              {...layout}>
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
                                       layout={layout}/>

                    <StoreInDBFormItem FormItem={FormItem} block={block} blockOptions={blockOptions}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={layout}/>

                </Form>


                {/*ADDING ANSWER*/}
                <Modal title="Add Answer" width={700} destroyOnClose={true} visible={this.state.modalVisible}
                       onOk={this.addAnswer} onCancel={this.hideAddAnswer}>
                    <Form>
                        <FormItem label="Answer"
                                  extra="This will be shown as answer in chatbot"
                                  {...layout}>
                            {getFieldDecorator('answer', {
                                rules: [{
                                    required: true,
                                    message: "Please input answer field",
                                }],
                            })(
                                <Input placeholder="Ex: Yes I need it :)"/>
                            )}
                        </FormItem>

                        <FormItem label="Keywords" {...layout}
                                  extra="Adding related keywords to the answer is necessary
                                  for retrieving accurate solutions to the user">
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
                                        <Icon type="plus"/> New Keyword
                                    </Tag>
                                )}
                            </div>
                        </FormItem>

                        <ActionFormItem FormItem={FormItem} blockOptions={blockOptions}
                                        block={block}
                                        setStateHandler={(state) => this.setState(state)}
                                        getFieldDecorator={getFieldDecorator}
                                        layout={layout}/>

                        <ShowGoToBlockFormItem FormItem={FormItem}
                                               block={block}
                                               allBlocks={allBlocks}
                                               showGoToBlock={this.state.showGoToBlock}
                                               getFieldDecorator={getFieldDecorator}
                                               layout={layout}/>

                        <ShowGoToGroupFormItem FormItem={FormItem}
                                               block={block}
                                               allGroups={allGroups}
                                               currentGroup={currentGroup}
                                               showGoToGroup={this.state.showGoToGroup}
                                               getFieldDecorator={getFieldDecorator}
                                               layout={layout}/>

                        <AfterMessageFormItem FormItem={FormItem} block={block}
                                              getFieldDecorator={getFieldDecorator}
                                              layout={layout}/>
                    </Form>

                </Modal>
            </Card>
        );
    }

}


export default Form.create()(Question);

