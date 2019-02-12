import React, {Component} from 'react';
import {Card, Form, Input} from "antd";
import {getInitialVariables, initActionType} from './CardTypesHelpers'
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    ShowGoToBlockFormItem,
    ShowGoToGroupFormItem,
    SkippableFormItem,
    StoreInDBFormItem
} from './CardTypesFormItems'

const FormItem = Form.Item;

class Solutions extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
        groupName: ''
    };

    componentWillMount() {
        this.handleNewBlock = this.props.handleNewBlock;
        this.handleEditBlock = this.props.handleEditBlock;
        this.handleDeleteBlock = this.props.handleDeleteBlock;

        const {allGroups, block} = getInitialVariables(this.props.options);
        this.setState(initActionType(block, allGroups));
    }

    onSubmit = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            const {flowOptions} = getInitialVariables(this.props.options);
            let options = {
                block: {
                    type: 'Solutions',
                    groupID: this.props.options.currentGroup.id,
                    storeInDB: false,
                    isSkippable: false,
                    dataType: flowOptions.dataTypes.find((dataType) => dataType.name === "No Type"),
                    content: {
                        showTop: Number(values.showTop),
                        action: values.action,
                        blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                        afterMessage: values.afterMessage,
                    }
                }
            };

            if (this.handleNewBlock)
                this.handleNewBlock(options);
            else {
                // Edit Block
                options.block.id = this.props.options.block.ID;
                options.block.order = this.props.options.block.Order;
                this.handleEditBlock(options);
            }
        }
    });


    render() {
        const {flowOptions, allGroups, allBlocks, blockOptions, block} = getInitialVariables(this.props.options, 'Solutions');
        const {getFieldDecorator} = this.props.form;

        const buttons = ButtonsForm(this.handleNewBlock, this.handleEditBlock, this.handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{width: '100%'}} actions={buttons}>
                <Form layout='horizontal'>

                    <FormItem label="Show Top Results"
                              extra="Number of results you want to return (Best matches e.g. Clients, Candidates, etc.)"
                              {...this.props.options.layout}>
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


                    <ActionFormItem FormItem={FormItem} blockOptions={blockOptions} block={block}
                                    setStateHandler={(state) => this.setState(state)}
                                    getFieldDecorator={getFieldDecorator}
                                    layout={this.props.options.layout}/>

                    <ShowGoToBlockFormItem FormItem={FormItem} allBlocks={allBlocks} block={block}
                                           showGoToBlock={this.state.showGoToBlock}
                                           getFieldDecorator={getFieldDecorator}
                                           layout={this.props.options.layout}/>

                    <ShowGoToGroupFormItem FormItem={FormItem} allGroups={allGroups} groupName={this.state.groupName}
                                           showGoToGroup={this.state.showGoToGroup}
                                           getFieldDecorator={getFieldDecorator}
                                           layout={this.props.options.layout}/>

                    <AfterMessageFormItem FormItem={FormItem} block={block}
                                          getFieldDecorator={getFieldDecorator}
                                          layout={this.props.options.layout}/>

                </Form>
            </Card>
        );
    }
}

export default Form.create()(Solutions);

