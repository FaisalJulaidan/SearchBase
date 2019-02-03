import React, {Component} from 'react';
import {Card, Form} from "antd";
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

class UserInput extends Component {

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
                    type: 'User Input',
                    groupID: this.props.options.currentGroup.id,
                    storeInDB: values.storeInDB,
                    isSkippable: values.isSkippable || false,
                    dataType: flowOptions.dataTypes.find((dataType) => dataType.name === values.dataType),
                    content: {
                        text: values.text,
                        blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                        action: values.action,
                        afterMessage: values.afterMessage
                    }
                }
            };

            if (this.handleNewBlock)
                this.handleNewBlock(options);
            else {
                // Edit Block
                options.block.id = this.props.options.block.id;
                options.block.order = this.props.options.block.order;
                this.handleEditBlock(options);
            }

        }
    });


    render() {
        const {flowOptions, allGroups, allBlocks, blockOptions, block} = getInitialVariables(this.props.options, 'User Input');
        const {getFieldDecorator} = this.props.form;

        const buttons = ButtonsForm(this.handleNewBlock, this.handleEditBlock, this.handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{width: '100%'}} actions={buttons}>
                <Form layout='horizontal'>
                    <QuestionFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={this.props.options.layout}
                                      placeholder="Ex: What is your email?"/>

                    <DataTypeFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator} flowOptions={flowOptions}
                                      layout={this.props.options.layout}/>

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

                    <SkippableFormItem FormItem={FormItem} block={block}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={this.props.options.layout}/>

                    <StoreInDBFormItem FormItem={FormItem} block={block} blockOptions={blockOptions}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={this.props.options.layout}/>

                </Form>
            </Card>
        );
    }
}

export default Form.create()(UserInput);