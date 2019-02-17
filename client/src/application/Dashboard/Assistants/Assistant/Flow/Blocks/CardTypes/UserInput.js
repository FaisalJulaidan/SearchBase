import React, {Component} from 'react';
import {Card, Form} from "antd";
import {getInitialVariables, initActionType, getBlockId} from './CardTypesHelpers'
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

class UserInput extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
    };

    componentDidMount() {
        const {modalState, options} = this.props;
        const {block} = getInitialVariables(options.flow, modalState);
        this.setState(initActionType(block, this.props.modalState.allGroups));
    }

    onSubmit = (formBlock) => this.props.form.validateFields((err, values) => {
        if (!err) {
            const flowOptions = this.props.options.flow;


            let options = {
                block: {
                    Type: 'User Input',
                    GroupID: this.props.modalState.currentGroup.id,
                    StoreInDB: values.storeInDB,
                    Skippable: values.isSkippable || false,
                    DataType: flowOptions.dataTypes.find((dataType) => dataType.name === values.dataType),
                    Content: {
                        text: values.text,
                        blockToGoID: getBlockId(values.blockToGoID, values.blockToGoIDGroup, this.props.modalState.currentGroup.blocks, formBlock),
                        action: values.action,
                        afterMessage: values.afterMessage || ""
                    }
                }
            };

            if (this.props.handleNewBlock)
                this.props.handleNewBlock(options);
            else {
                // Edit Block
                options.block.ID = this.props.modalState.block.ID;
                options.block.Order = this.props.modalState.block.Order;
                this.props.handleEditBlock(options);
            }

        }
    });


    render() {
        const {modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock} = this.props;
        const {blockOptions, block} = getInitialVariables(options.flow ,modalState, 'User Input');
        const {allGroups, allBlocks, currentGroup, layout} = modalState;
        const {getFieldDecorator} = form;


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
                                           currentBlock={block}
                                           allGroups={allGroups}
                                           currentGroup={currentGroup}
                                           showGoToGroup={this.state.showGoToGroup}
                                           getFieldDecorator={getFieldDecorator}
                                           layout={layout}/>

                    <AfterMessageFormItem FormItem={FormItem} block={block}
                                          getFieldDecorator={getFieldDecorator}
                                          layout={layout}/>

                    <SkippableFormItem FormItem={FormItem} block={block}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={layout}/>

                    <StoreInDBFormItem FormItem={FormItem} block={block} blockOptions={blockOptions}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={layout}/>

                </Form>
            </Card>
        );
    }
}

export default Form.create()(UserInput);