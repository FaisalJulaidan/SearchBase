import React, { Component } from 'react';
import { Card, Divider, Form, Icon, Input, Tag, Tooltip } from 'antd';
import { getInitialVariables, initActionType, initActionTypeSkip } from './CardTypesHelpers';
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    DataTypeFormItem,
    QuestionFormItem,
    ShowGoToBlockFormItem,
    ShowGoToBlockSkipFormItem,
    ShowGoToGroupFormItem,
    ShowGoToGroupSkipFormItem,
    SkipFormItem,
    SkippableFormItem,
    SkipTextFormItem,
    StoreInDBFormItem
} from './FormItems';

const FormItem = Form.Item;

class UserInput extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,

        showGoToBlockSkip: false,
        showGoToGroupSkip: false,

        tags: [],
        inputVisible: false,
        inputValue: '',

    };

    componentDidMount() {
        const { modalState, options } = this.props;
        const { block } = getInitialVariables(options.flow, modalState);
        this.setState({
            ...initActionType(block, this.props.modalState.allGroups),
            ...initActionTypeSkip(block, this.props.modalState.allGroups),
            showSkip: block.Skippable || false,
            tags: block.Content.keywords || []
        });
    }

    onSubmit = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            const flowOptions = this.props.options.flow;
            let options = {
                Type: 'User Input',
                StoreInDB: values.storeInDB,

                Skippable: values.isSkippable || false,
                SkipText: values.SkipText || "Skip!",
                SkipAction: values.SkipAction || "End Chat",
                SkipBlockToGoID: values.skipBlockToGoID || values.skipBlockToGoIDGroup || null,

                DataType: flowOptions.dataTypes
                    .find((dataType) => dataType.name === values.dataType[values.dataType.length-1]),
                Content: {
                    text: values.text,
                    blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                    action: values.action,
                    afterMessage: values.afterMessage || "",
                    keywords: this.state.tags || []
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

    render() {
        const {modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock} = this.props;
        const {blockOptions, block} = getInitialVariables(options.flow ,modalState, 'User Input');
        const {allGroups, allBlocks, currentGroup, layout} = modalState;
        const {getFieldDecorator} = form;

        const {tags, inputVisible, inputValue, showSkip} = this.state;

        const buttons = ButtonsForm(handleNewBlock, handleEditBlock, handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{width: '100%'}} actions={buttons}>
                <Form layout='horizontal'>
                    <QuestionFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={layout}
                                      placeholder="Ex: What is your email?"/>

                    <DataTypeFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      options={this.props.options}
                                      layout={layout}
                                      blockType={"User Input"}/>

                    <FormItem label="Scoring Keywords" {...layout}
                              extra="Every matched keyword from user input will add up to the score">
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

                    <ActionFormItem FormItem={FormItem} blockOptions={blockOptions} block={block}
                                    setStateHandler={(state) => this.setState(state)}
                                    getFieldDecorator={getFieldDecorator}
                                    layout={layout}/>

                    <ShowGoToBlockFormItem FormItem={FormItem} allBlocks={allBlocks} block={block}
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


                    <StoreInDBFormItem FormItem={FormItem} block={block} blockOptions={blockOptions}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={layout}/>

                    <SkippableFormItem FormItem={FormItem} block={block}
                                       setStateHandler={(state) => this.setState(state)}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={layout}/>
                    {
                        showSkip &&
                        <>
                            <Divider dashed={true} style={{fontWeight: 'normal', fontSize: '14px'}}>
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
            </Card>
        );
    }
}

export default Form.create()(UserInput);
