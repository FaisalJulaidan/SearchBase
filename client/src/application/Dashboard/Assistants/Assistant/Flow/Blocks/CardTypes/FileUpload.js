import React, {Component} from 'react';
import {Card, Form} from "antd";

import {getInitialVariables, initActionType} from './CardTypesHelpers'
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    DataCategoryFormItem,
    FileTypesFormItem,
    QuestionFormItem,
    ShowGoToBlockFormItem,
    ShowGoToGroupFormItem,
    SkippableFormItem
} from './CardTypesFormItems'

const FormItem = Form.Item;

class FileUpload extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
        fileTypes: [],
        groupName: ''
    };

    onSubmit = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            let options = {
                block: {
                    type: 'File Upload',
                    groupID: this.props.options.currentGroup.id,
                    storeInDB: true,
                    isSkippable: values.isSkippable,
                    dataCategoryID: values.dataCategoryID,
                    content: {
                        text: values.text,
                        action: values.action,
                        fileTypes: this.state.fileTypes,
                        blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
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

    componentWillMount() {
        this.handleNewBlock = this.props.handleNewBlock;
        this.handleEditBlock = this.props.handleEditBlock;
        this.handleDeleteBlock = this.props.handleDeleteBlock;

        const {allGroups, block} = getInitialVariables(this.props.options);
        this.setState(initActionType(block, allGroups));
    }


    render() {
        const {flowOptions, allGroups, allBlocks, blockOptions, block} = getInitialVariables(this.props.options, 'File Upload');
        const {getFieldDecorator} = this.props.form;
        const {typesAllowed} = blockOptions;

        const buttons = ButtonsForm(this.handleNewBlock, this.handleEditBlock, this.handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{width: '100%'}} actions={buttons}>
                <Form layout='horizontal'>
                    <QuestionFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={this.props.options.layout}/>

                    <DataCategoryFormItem FormItem={FormItem} block={block}
                                          getFieldDecorator={getFieldDecorator} flowOptions={flowOptions}
                                          layout={this.props.options.layout}/>

                    <FileTypesFormItem FormItem={FormItem} typesAllowed={typesAllowed} block={block}
                                       setStateHandler={(state) => this.setState(state)}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={this.props.options.layout}/>

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

                    <SkippableFormItem FormItem={FormItem} block={block}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={this.props.options.layout}/>
                </Form>
            </Card>
        );
    }
}

export default Form.create()(FileUpload);

