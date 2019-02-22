import React, {Component} from 'react';
import {Card, Form, Input} from "antd";
import {getBlockId, getInitialVariables, initActionType} from './CardTypesHelpers'
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    ShowGoToBlockFormItem,
    ShowGoToGroupFormItem,
    DatabaseTypeFormItem
} from './CardTypesFormItems'

const FormItem = Form.Item;

class Solutions extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
    };

    componentWillMount() {
        const {modalState, options} = this.props;
        const {block} = getInitialVariables(options.flow, modalState);
        this.setState(initActionType(block, this.props.modalState.allGroups));
    }

    onSubmit = (formBlock) => this.props.form.validateFields((err, values) => {
        if (!err) {
            const flowOptions = this.props.options.flow;
            let options = {
                    Type: 'Solutions',
                    GroupID: this.props.modalState.currentGroup.id,
                    StoreInDB: false,
                    Skippable: false,
                    DataType: flowOptions.dataTypes.find((dataType) => dataType.name === "No Type"),
                    Content: {
                        showTop: Number(values.showTop),
                        action: values.action,
                        blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                        afterMessage: values.afterMessage || "" ,
                        databaseType: values.databaseType,
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
        const {blockOptions, block} = getInitialVariables(options.flow ,modalState, 'Solutions');
        const {allGroups, allBlocks, currentGroup, layout} = modalState;
        const {getFieldDecorator} = form;

        const buttons = ButtonsForm(handleNewBlock, handleEditBlock, handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{width: '100%'}} actions={buttons}>
                <Form layout='horizontal'>

                    <FormItem label="Show Top Results"
                              extra="Number of results you want to return (Best matches e.g. Clients, Candidates, etc.)"
                              {...layout}>
                        {getFieldDecorator('showTop', {
                            initialValue: block.Content.showTop,
                            rules: [{
                                required: true,
                                message: "Please set how many solutions to return",
                            }],
                        })(
                            <Input min="1" type="number" placeholder="Ex: 5"/>
                        )}
                    </FormItem>

                    <DatabaseTypeFormItem FormItem={FormItem} block={block}
                                          getFieldDecorator={getFieldDecorator}
                                          layout={layout}
                                          options={this.props.options}/>

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

                </Form>
            </Card>
        );
    }
}

export default Form.create()(Solutions);

