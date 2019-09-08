import React, { Component } from 'react';
import { Card, Divider, Form, Select, Spin } from 'antd';

import { getInitialVariables, initActionType, initActionTypeSkip } from './CardTypesHelpers';
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    QuestionFormItem,
    ShowGoToBlockFormItem,
    ShowGoToBlockSkipFormItem,
    ShowGoToGroupFormItem,
    ShowGoToGroupSkipFormItem,
    SkipFormItem,
    SkippableFormItem,
    SkipTextFormItem
} from './FormItems';

const FormItem = Form.Item;
const Option = Select.Option;

class JobType extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false
    };

    onSubmit = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            let options = {
                Type: 'Job Type',
                StoreInDB: false,

                Skippable: values.isSkippable || false,
                SkipText: values.SkipText || 'Skip!',
                SkipAction: values.SkipAction || 'End Chat',
                SkipBlockToGoID: values.skipBlockToGoID || values.skipBlockToGoIDGroup || null,

                DataType: 'JobType',
                Content: {
                    text: values.text,
                    action: values.action,
                    blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null
                }
            };
            console.log(options);

            if (this.props.handleNewBlock)
                this.props.handleNewBlock(options);
            else {
                // Edit Block
                options.ID = this.props.modalState.block.ID;
                this.props.handleEditBlock(options);
            }
        }
    });

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

    componentWillMount() {
        const { modalState, options } = this.props;
        const { block } = getInitialVariables(options.flow, modalState);
        this.setState(initActionType(block, this.props.modalState.allGroups));
    }


    render() {
        const { modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock } = this.props;
        const { blockOptions, block } = getInitialVariables(options.flow, modalState, 'Job Type');
        const { allGroups, allBlocks, currentGroup, layout } = modalState;
        const { getFieldDecorator } = form;
        const { showSkip } = this.state;

        const buttons = ButtonsForm(handleNewBlock, handleEditBlock, handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{ width: '100%' }} actions={buttons}>
                <Form layout='horizontal'>


                    <QuestionFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={layout}
                                      placeholder="Ex: What is your job?"/>

                    <FormItem label="Available Types"
                              extra="123"
                              {...layout}>
                        {
                            blockOptions.types?.length > 0 ?
                                getFieldDecorator('availableTypes', {
                                    initialValue: block.Content.availableTypes ? block.Content.availableTypes : undefined,
                                    rules: [{
                                        required: true,
                                        message: 'Please input a question'
                                    }]
                                })(
                                    <Select placeholder="Select one of the available types">
                                        {
                                            blockOptions.types.map((type, i) => <Option key={i}
                                                                                        value={type}>{type}</Option>)
                                        }
                                    </Select>
                                )
                                : <Spin><Select placeholder="Select one of the available types"></Select></Spin>
                        }
                    </FormItem>

                    <AfterMessageFormItem FormItem={FormItem} block={block}
                                          getFieldDecorator={getFieldDecorator}
                                          layout={layout}/>

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

                    <SkippableFormItem FormItem={FormItem} block={block}
                                       setStateHandler={(state) => this.setState(state)}
                                       getFieldDecorator={getFieldDecorator}
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
            </Card>
        );
    }
}

export default Form.create()(JobType);

