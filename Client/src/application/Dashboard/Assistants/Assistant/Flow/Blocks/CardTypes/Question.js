import React, { Component } from 'react';
import { Button, Card, Collapse, Divider, Form, Icon, Input, Modal, Popconfirm, Tag, Tooltip, Typography } from 'antd';

import { getInitialVariables, initActionType, initActionTypeSkip } from './CardTypesHelpers';
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    DataTypeFormItem,
    QuestionFormItem,
    ScoreFormItem,
    ShowGoToBlockFormItem,
    ShowGoToBlockSkipFormItem,
    ShowGoToGroupFormItem,
    ShowGoToGroupSkipFormItem,
    SkipFormItem,
    SkippableFormItem,
    SkipTextFormItem,
    StoreInDBFormItem
} from './FormItems';
import shortid from 'shortid';
import './CardTypes.less';

const { Paragraph } = Typography;

const FormItem = Form.Item;

class Question extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,

        showGoToBlockSkip: false,
        showGoToGroupSkip: false,

        modalVisible: false,

        tags: [],
        inputVisible: false,
        inputValue: '',
        answers: [],
        editedAnswer: {},

        groupName: '',
        showSkip: false
    };

    //Submit whole block
    onSubmit = () => this.props.form.validateFields(['text', 'isSkippable', 'storeInDB', 'dataType', 'SkipText', 'SkipAction', 'skipBlockToGoID', 'skipBlockToGoIDGroup'],
        (err, values) => {
            if (!err) {
                const flowOptions = this.props.options.flow;
                let options = {
                    Type: 'Question',
                    StoreInDB: values.storeInDB,

                    Skippable: values.isSkippable || false,
                    SkipText: values.SkipText || 'Skip!',
                    SkipAction: values.SkipAction || 'End Chat',
                    SkipBlockToGoID: values.skipBlockToGoID || values.skipBlockToGoIDGroup || null,

                    DataType: flowOptions.dataTypes
                        .find((dataType) => dataType.name === values.dataType[values.dataType.length - 1]),
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
    addAnswer = () => this.props.form.validateFields(['answer', 'action', 'blockToGoID', 'blockToGoIDGroup', 'afterMessage', 'scoreWeight'],
        (err, values) => {
            if (!err) {
                const answer = {
                    id: shortid.generate(),
                    text: values.answer,
                    keywords: this.state.tags,
                    blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                    action: values.action,
                    afterMessage: values.afterMessage || '',
                    score: values.scoreWeight || 0
                };

                // remove old edited answer
                this.removeAnswer({ id: this.state.editedAnswer?.id })
                    .then(() => {
                        let answers = [answer].concat(this.state.answers);
                        this.setState({ answers, tags: [] });
                        this.hideAddAnswer();
                    });
            }
        });
    showAddAnswer = () => this.setState({ modalVisible: true });
    hideAddAnswer = () => this.setState({ modalVisible: false, editedAnswer: {}, tags: [] });
    removeAnswer = deletedAnswer => new Promise(res => {
        this.setState({
            answers: [...this.state.answers].filter(answer => answer.id !== deletedAnswer.id)
        }, () => res('done'));
    });

    showEditAnswer = answer => this.setState({
        modalVisible: true, editedAnswer: answer, tags: answer.keywords,
        ...initActionType({ Content: answer }, this.props.modalState.allGroups)
    });

    //Tags component's functions
    removeTag = (removedTag) => this.setState({ tags: this.state.tags.filter(tag => tag !== removedTag) });
    showInput = () => this.setState({ inputVisible: true }, () => this.input.focus());
    handleInputChange = e => this.setState({ inputValue: e.target.value });
    saveInputRef = input => this.input = input;
    handleInputConfirm = () => {
        const inputValue = this.state.inputValue;
        let tags = this.state.tags;
        if (inputValue && tags.indexOf(inputValue) === -1)
            tags = [...tags, inputValue];
        this.setState({ tags, inputVisible: false, inputValue: '' });
    };


    componentWillMount() {
        const { modalState, options } = this.props;
        const { block } = getInitialVariables(options.flow, modalState);
        this.setState({
            ...initActionType(block, this.props.modalState.allGroups),
            ...initActionTypeSkip(block, this.props.modalState.allGroups),
            answers: block.Content.answers || [],
            showSkip: block.Skippable || false
        });
    }

    render() {
        const { modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock } = this.props;
        const { blockOptions, block } = getInitialVariables(options.flow, modalState, 'Question');
        const { allGroups, allBlocks, currentGroup, layout } = modalState;
        const { getFieldDecorator } = form;

        const { tags, inputVisible, inputValue, showSkip } = this.state;

        const buttons = ButtonsForm(handleNewBlock, handleEditBlock, handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{ width: '100%' }} actions={buttons}>
                <Form layout='horizontal' id={'Flow_Questions'}>
                    <QuestionFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={layout}
                                      placeholder="Ex: What best describes you?"/>

                    <DataTypeFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      options={this.props.options}
                                      layout={layout}
                                      blockType={'Question'}/>

                    <FormItem label="Answers"{...layout}>
                        <Button onClick={this.showAddAnswer} type="primary" icon="plus" size={'small'}>Add
                            Answer</Button>
                        <Collapse accordion>
                            {
                                this.state.answers.map((answer, i) => (
                                    <Collapse.Panel
                                        header={
                                            <Paragraph style={{ width: 'calc(100% - 85px)', margin: 0 }}
                                                       ellipsis={{ rows: 1 }}>
                                                {answer.text}
                                            </Paragraph>
                                        }
                                        key={i}
                                        extra={
                                            <div>
                                                <Button type="default" icon="edit"
                                                        onClick={(event) => {
                                                            this.showEditAnswer(answer);
                                                            event.stopPropagation();
                                                        }}
                                                        size={'small'}></Button>
                                                <Popconfirm placement="topRight"
                                                            title="Are you sure delete this answer?"
                                                            onConfirm={(event) => {
                                                                this.removeAnswer(answer);
                                                                event.stopPropagation();
                                                            }}
                                                            okText="Yes" cancelText="No">
                                                    <Button type="danger" icon="delete"
                                                            onClick={(event) => event.stopPropagation()}
                                                            style={{ marginLeft: 5 }}
                                                            size={'small'}></Button>
                                                </Popconfirm>
                                            </div>
                                        }>
                                        <p>Action: {answer.action}</p>
                                        Keywords: <br/>
                                        {answer.keywords.map((keyword, i) => <Tag key={i}>{keyword}</Tag>)}
                                    </Collapse.Panel>
                                ))
                            }
                        </Collapse>
                    </FormItem>


                    <StoreInDBFormItem FormItem={FormItem} block={block} blockOptions={blockOptions}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={layout}/>

                    <SkippableFormItem FormItem={FormItem} block={block}
                                       getFieldDecorator={getFieldDecorator}
                                       setStateHandler={(state) => this.setState(state)}
                                       layout={layout}/>

                    {
                        showSkip &&
                        <>
                            <Divider dashed={true} style={{ fontWeight: 'normal', fontSize: '14px' }}>
                                Skip Button
                            </Divider>


                            <SkipTextFormItem FormItem={FormItem}
                                              layout={layout}
                                              getFieldDecorator={getFieldDecorator}
                                              block={block}/>


                            <SkipFormItem FormItem={FormItem}
                                          blockOptions={blockOptions}
                                          block={block} layout={layout}
                                          setStateHandler={(state) => this.setState(state)}
                                          getFieldDecorator={getFieldDecorator}/>

                            <ShowGoToBlockSkipFormItem FormItem={FormItem} allBlocks={allBlocks} block={block}
                                                       showGoToBlock={this.state.showGoToBlockSkip}
                                                       getFieldDecorator={getFieldDecorator}
                                                       layout={layout}/>

                            <ShowGoToGroupSkipFormItem FormItem={FormItem}
                                                       block={block}
                                                       allGroups={allGroups}
                                                       currentGroup={currentGroup}
                                                       showGoToGroup={this.state.showGoToGroupSkip}
                                                       getFieldDecorator={getFieldDecorator}
                                                       layout={layout}/>
                        </>
                    }
                </Form>


                {/*ADDING ANSWER*/}
                <Modal title="Add Answer" width={700} destroyOnClose={true} visible={this.state.modalVisible}
                       onOk={this.addAnswer} onCancel={this.hideAddAnswer}>
                    <Form>
                        <FormItem label="Answer"
                                  extra="This will be shown as answer in chatbot"
                                  {...layout}>
                            {getFieldDecorator('answer', {
                                initialValue: this.state.editedAnswer?.text,
                                rules: [{
                                    required: true,
                                    message: 'Please input answer field'
                                }]
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
                                        <Tag key={tag} closable={true} onClose={() => this.removeTag(tag)}>
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
                                        style={{ width: 78 }}
                                        value={inputValue}
                                        onChange={this.handleInputChange}
                                        onBlur={this.handleInputConfirm}
                                        onPressEnter={this.handleInputConfirm}
                                    />
                                )}
                                {!inputVisible && (
                                    <Tag
                                        onClick={this.showInput}
                                        style={{ background: '#fff', borderStyle: 'dashed' }}>
                                        <Icon type="plus"/> New Keyword
                                    </Tag>
                                )}
                            </div>
                        </FormItem>

                        <ScoreFormItem FormItem={FormItem} layout={layout} getFieldDecorator={getFieldDecorator}
                                       block={{ Content: { ID: block.ID, score: this.state.editedAnswer?.score } }}/>

                        <ActionFormItem FormItem={FormItem}
                                        blockOptions={blockOptions}
                                        block={{ Content: { ID: block.ID, action: this.state.editedAnswer?.action } }}
                                        setStateHandler={(state) => this.setState(state)}
                                        getFieldDecorator={getFieldDecorator}
                                        layout={layout}/>

                        <ShowGoToBlockFormItem FormItem={FormItem}
                                               block={{
                                                   ID: block.ID,
                                                   Content: {
                                                       blockToGoID: this.state.editedAnswer?.blockToGoID
                                                   }
                                               }}
                                               allBlocks={allBlocks}
                                               showGoToBlock={this.state.showGoToBlock}
                                               getFieldDecorator={getFieldDecorator}
                                               layout={layout}/>

                        <ShowGoToGroupFormItem FormItem={FormItem}
                                               block={{
                                                   ID: block.ID,
                                                   Content: {
                                                       blockToGoID: this.state.editedAnswer?.blockToGoID
                                                   }
                                               }}
                                               allGroups={allGroups}
                                               currentGroup={currentGroup}
                                               showGoToGroup={this.state.showGoToGroup}
                                               getFieldDecorator={getFieldDecorator}
                                               layout={layout}/>

                        <AfterMessageFormItem FormItem={FormItem}
                                              block={{
                                                  ID: block.ID,
                                                  Content: {
                                                      afterMessage: this.state.editedAnswer?.afterMessage
                                                  }
                                              }}
                                              getFieldDecorator={getFieldDecorator}
                                              layout={layout}/>
                    </Form>

                </Modal>
            </Card>
        );
    }

}


export default Form.create()(Question);

