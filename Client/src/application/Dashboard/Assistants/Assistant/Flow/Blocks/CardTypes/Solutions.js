import React, {Component} from 'react';
import {Card, Form, Input, Divider} from "antd";
import {initActionTypeSkip, getInitialVariables, initActionType} from './CardTypesHelpers'
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    ShowGoToBlockFormItem,
    ShowGoToGroupFormItem,
    DatabaseTypeFormItem,
    SkipFormItem,
    ShowGoToBlockSkipFormItem,
    ShowGoToGroupSkipFormItem, SkippableFormItem, SkipTextFormItem
} from './FormItems'

const FormItem = Form.Item;

class Solutions extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,

        showGoToBlockSkip: false,
        showGoToGroupSkip: false,

    };

    componentWillMount() {
        const {modalState, options} = this.props;
        const {block} = getInitialVariables(options.flow, modalState);

        this.setState({
            ...initActionType(block, this.props.modalState.allGroups),
            ...initActionTypeSkip(block, this.props.modalState.allGroups),
            showSkip: block.Skippable || true
        });
    }

    onSubmit = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            const flowOptions = this.props.options.flow;
            const showTop = Number(values.showTop) > 10 ? 10 : Number(values.showTop);
            let options = {
                Type: 'Solutions',
                StoreInDB: true,

                Skippable: values.isSkippable || false,
                SkipText: values.SkipText || "Skip!",
                SkipAction: values.SkipAction || "End Chat",
                SkipBlockToGoID: values.skipBlockToGoID || values.skipBlockToGoIDGroup || null,

                DataType: flowOptions.dataTypes.find((dataType) => dataType.name === "No Type"),
                Content: {
                    showTop: showTop,
                    action: values.action,
                    blockToGoID: values.blockToGoID || values.blockToGoIDGroup || null,
                    afterMessage: values.afterMessage || "",
                    databaseType: values.databaseType,
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


    render() {
        const {modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock} = this.props;
        const {blockOptions, block} = getInitialVariables(options.flow ,modalState, 'Solutions');
        const {allGroups, allBlocks, currentGroup, layout} = modalState;
        const {getFieldDecorator} = form;

        const buttons = ButtonsForm(handleNewBlock, handleEditBlock, handleDeleteBlock, this.onSubmit, block);

        const {showSkip} = this.state;

        return (
            <Card style={{width: '100%'}} actions={buttons}>
                <Form layout='horizontal'>

                    <FormItem label="Show Top Results"
                              extra="Number of results you want to return (Best matches e.g. Clients, Candidates, etc.) max: 20"
                              {...layout}>
                        {getFieldDecorator('showTop', {
                            initialValue: block.Content.showTop || 5,
                            rules: [{
                                required: true,
                                message: "Please set how many solutions to return",
                            }],
                        })(
                            <Input min="1" max="20" type="number" placeholder="Ex: 5"/>
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

                    <SkippableFormItem FormItem={FormItem} block={block}
                                       label={'When Not Found'}
                                       toShow={true}
                                       setStateHandler={(state) => this.setState(state)}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={layout}/>

                    {
                        showSkip &&
                        <>
                            <Divider dashed={true} style={{fontWeight: 'normal', fontSize: '14px'}}>
                                Not Found Button
                            </Divider>

                            <SkipTextFormItem FormItem={FormItem}
                                              layout={layout}
                                              getFieldDecorator={getFieldDecorator}
                                              block={block}
                                              text={`Not found what you're looking for?`}/>

                            <SkipFormItem FormItem={FormItem}
                                          blockOptions={blockOptions}
                                          label={'Not Found Action'}
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

export default Form.create()(Solutions);

