import React, {Component} from 'react';
import {Card, Checkbox, Form, Select, Spin} from "antd";

import {getInitialVariables, initActionType, onChange} from './CardTypesHelpers'
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    QuestionFormItem,
    SkippableFormItem
} from './CardTypesFormItems'

const FormItem = Form.Item;
const Option = Select.Option;
const CheckboxGroup = Checkbox.Group;

class FileUpload extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
        fileTypes: [],
        groupName: ''
    };

    setStateHandler = (state) => this.setState(state);

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
                    <QuestionFormItem block={block} FormItem={FormItem}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={{...this.props.options.layout}}/>

                    <FormItem label="Data Category"
                              extra="Categorising users' responses will result in  more efficient AI processing"
                              {...this.props.options.layout}>
                        {
                            getFieldDecorator('dataCategoryID', {
                                initialValue: null || block.dataCategoryID,
                                rules: [{
                                    required: true,
                                    message: "Please specify the data category",
                                }]
                            })(
                                <Select placeholder="Will validate the input">
                                    {
                                        flowOptions.dataCategories.map((category, i) =>
                                            <Option key={i} value={category.ID}>{category.Name}</Option>)
                                    }
                                </Select>
                            )
                        }
                    </FormItem>

                    <FormItem label="File Types"
                              {...this.props.options.layout}>
                        {
                            blockOptions.typesAllowed ?
                                getFieldDecorator('fileTypes', {
                                    initialValue: block.content.fileTypes,
                                    rules: [{
                                        required: true,
                                        message: "Please select the accepted file type",
                                    }]
                                })(
                                    <CheckboxGroup options={typesAllowed}
                                                   onChange={(checkedValues) => this.setState(onChange(checkedValues))}/>
                                )
                                : <Spin/>
                        }
                    </FormItem>

                    <ActionFormItem block={block} FormItem={FormItem} onSubmit={this.onSubmit}
                                    blockOptions={blockOptions}
                                    setStateHandler={(state) => this.setStateHandler(state)}
                                    getFieldDecorator={getFieldDecorator}
                                    layout={{...this.props.options.layout}}/>

                    {this.state.showGoToBlock ?
                        (<FormItem label="Go To Specific Block" {...this.props.options.layout}>
                            {
                                getFieldDecorator('blockToGoID',
                                    {
                                        initialValue: block.content.blockToGoID,
                                        rules: [{required: true, message: "Please select your next block"}]
                                    }
                                )(
                                    <Select placeholder="The next step after this block">{
                                        allBlocks.map((block, i) =>
                                            <Option key={i} value={block.id}>
                                                {`${block.id}- (${block.type}) ${block.content.text ? block.content.text : ''}`}
                                            </Option>
                                        )
                                    }</Select>
                                )
                            }
                        </FormItem>)
                        : null
                    }

                    {this.state.showGoToGroup ?
                        (<FormItem label="Go To Specific Group"
                                   extra="The selected group will start from its first block"
                                   {...this.props.options.layout}>
                            {
                                getFieldDecorator('blockToGoIDGroup',
                                    {
                                        initialValue: this.state.groupName,
                                        rules: [{required: true, message: "Please select your next group"}]
                                    }
                                )(
                                    <Select placeholder="The next block after this block">{
                                        allGroups.map((group, i) => {
                                                if (group.blocks[0])
                                                    return <Option key={i} value={group.blocks[0].id}>
                                                        {`${group.name}`}
                                                    </Option>;
                                                else
                                                    return <Option disabled key={i} value={group.name}>
                                                        {`${group.name}`}
                                                    </Option>
                                            }
                                        )
                                    }</Select>
                                )
                            }
                        </FormItem>)
                        : null
                    }

                    <AfterMessageFormItem block={block} FormItem={FormItem}
                                          getFieldDecorator={getFieldDecorator}
                                          layout={{...this.props.options.layout}}/>


                    <SkippableFormItem block={block} FormItem={FormItem}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={{...this.props.options.layout}}/>
                </Form>
            </Card>
        );
    }
}

export default Form.create()(FileUpload);

