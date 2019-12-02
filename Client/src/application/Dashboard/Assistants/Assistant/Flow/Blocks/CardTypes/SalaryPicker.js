import React, { Component } from 'react';
import { Card, Divider, Form } from 'antd';

import { getInitialVariables, initActionType, initActionTypeSkip } from './CardTypesHelpers';
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    DataTypeFormItem,
    DefualtCurrencyFormItem,
    MinMaxSalaryFormItem,
    PayPeriodFormItem,
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

class SalaryPicker extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
        showSkip: false
    };

    onSubmit = async () => {
        const isFilled = await this.minMaxSalaryFormItem.checkFields();
        this.props.form.validateFields((err, values) => {
            if (!err && isFilled) {
                const flowOptions = this.props.options.flow;
                let options = {
                    Type: 'Salary Picker',
                    StoreInDB: false,

                    Skippable: values.isSkippable || false,
                    SkipText: values.SkipText || 'Skip!',
                    SkipAction: values.SkipAction || 'End Chat',
                    SkipBlockToGoID: values.skipBlockToGoID || values.skipBlockToGoIDGroup || null,

                    DataType: flowOptions.dataTypes
                        .find((dataType) => dataType.name === values.dataType[values.dataType.length - 1]),
                    Content: {
                        text: values.text,
                        min: +values.minSalary,
                        max: +values.maxSalary,
                        period: values.payPeriod,
                        currency: values.currency,
                        action: values.action,
                        afterMessage: values.afterMessage || '',
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
    };

    componentWillMount() {
        const { modalState, options } = this.props;
        const { block } = getInitialVariables(options.flow, modalState);
        this.setState({
            ...initActionType(block, this.props.modalState.allGroups),
            ...initActionTypeSkip(block, this.props.modalState.allGroups),
            showSkip: block.Skippable || false
        });
    }

    render() {
        const { modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock } = this.props;
        const { blockOptions, block } = getInitialVariables(options.flow, modalState, 'Salary Picker');
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
                                      placeholder="Ex: What is your desired salary?"/>

                    <DataTypeFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      options={this.props.options}
                                      layout={layout}
                                      blockType={'Salary Picker'}/>

                    <MinMaxSalaryFormItem onRef={ref => (this.minMaxSalaryFormItem = ref)}
                                          FormItem={FormItem} layout={layout}
                                          block={block}
                                          getFieldDecorator={getFieldDecorator}
                                          form={this.props.form} options={this.props.options}/>

                    <DefualtCurrencyFormItem FormItem={FormItem} layout={layout}
                                             block={block}
                                             currencyCodes={options.databases.currencyCodes}
                                             getFieldDecorator={getFieldDecorator}/>

                    <PayPeriodFormItem FormItem={FormItem} block={block}
                                       getFieldDecorator={getFieldDecorator} layout={layout}/>

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
            </Card>
        );
    }
}

export default Form.create()(SalaryPicker);

