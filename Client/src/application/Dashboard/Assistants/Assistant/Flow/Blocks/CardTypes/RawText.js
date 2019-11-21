import React, {Component} from 'react';
import {Card, Form} from "antd";

import {getInitialVariables, initActionType} from './CardTypesHelpers'
import {
    ActionFormItem,
    ButtonsForm,
    RawTextFormItem,
    ShowGoToBlockFormItem,
    ShowGoToGroupFormItem,
} from './FormItems'

const FormItem = Form.Item;

class RawText extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
    };

    onSubmit = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            const flowOptions = this.props.options.flow;
            let options = {
                Type: 'Raw Text',
                StoreInDB: false,

                Skippable: values.isSkippable || false,
                SkipText: values.SkipText || "Skip!",
                SkipAction: values.SkipAction || "End Chat",
                SkipBlockToGoID: values.skipBlockToGoID || values.skipBlockToGoIDGroup || null,

                DataType: flowOptions.dataTypes.find((dataType) => dataType.name === "No Type"),
                Content: {
                    text: values.rawText,
                    action: values.action,
                    blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
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

    componentWillMount() {
        const {modalState, options} = this.props;
        const {block} = getInitialVariables(options.flow, modalState);
        this.setState(initActionType(block, this.props.modalState.allGroups));
    }


    render() {
        const {modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock} = this.props;
        const {blockOptions, block} = getInitialVariables(options.flow, modalState, 'Raw Text');
        const {allGroups, allBlocks, currentGroup, layout} = modalState;
        const {getFieldDecorator} = form;

        const buttons = ButtonsForm(handleNewBlock, handleEditBlock, handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{width: '100%'}} actions={buttons}>
                <Form layout='horizontal'>

                    <RawTextFormItem FormItem={FormItem} block={block}
                                     getFieldDecorator={getFieldDecorator}
                                     layout={layout}
                                     placeholder="Type your raw text here"/>


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
                </Form>
            </Card>
        );
    }
}

export default Form.create()(RawText);

