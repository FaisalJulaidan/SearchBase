import {Button, Checkbox, Input, Select, Spin} from "antd";
import React from 'react';
import {onCancel, onChange, onDelete, onSelectAction} from "./CardTypesHelpers";

const Option = Select.Option;
const CheckboxGroup = Checkbox.Group;

export const QuestionFormItem = ({FormItem, layout, getFieldDecorator, block}) => (
    <FormItem label="Question"
              extra="The above text will be shown in a bubble inside the chat"
              {...layout}>
        {getFieldDecorator('text', {
            initialValue: block.content.text,
            rules: [{
                required: true,
                message: "Please input question field",
            }],
        })(
            <Input placeholder="Ex: Please upload you cv"/>
        )}
    </FormItem>
);

export const DataCategoryFormItem = ({FormItem, layout, getFieldDecorator, flowOptions, block}) => (
    <FormItem label="Data Category"
              extra="Categorising users' responses will result in  more efficient AI processing"
              {...layout}>
        {
            getFieldDecorator('dataCategoryID', {
                initialValue: block.dataCategoryID ? block.dataCategoryID : undefined,
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
);

export const FileTypesFormItem = ({FormItem, layout, getFieldDecorator, typesAllowed, block}) => (
    <FormItem label="File Types" {...layout}>
        {
            typesAllowed ?
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
);

export const SkippableFormItem = ({FormItem, layout, getFieldDecorator, block}) => (
    <FormItem label="Skippable?" {...layout}>
        {getFieldDecorator('isSkippable', {
            valuePropName: 'checked',
            initialValue: block.isSkippable ? block.isSkippable : undefined,
        })(
            <Checkbox>Users can skip answering this question</Checkbox>
        )}
    </FormItem>
);

export const AfterMessageFormItem = ({FormItem, layout, getFieldDecorator, block}) => (
    <FormItem label="After message"
              extra="This message will display straight after the user's response"
              {...layout}>
        {getFieldDecorator('afterMessage', {
            initialValue: block.content.afterMessage ? block.content.afterMessage : undefined,
            rules: [{
                required: true,
                message: "Please input question field",
            }],
        })(
            <Input placeholder="Ex: Your input is recorded"/>
        )}
    </FormItem>
);

export const ActionFormItem = ({FormItem, layout, getFieldDecorator, setStateHandler, blockOptions, block}) => (
    <FormItem label="Action" {...layout}>
        {
            blockOptions.actions ?
                getFieldDecorator('action', {
                    initialValue: block.content.action ? block.content.action : undefined,
                    rules: [{
                        required: true,
                        message: "Please input question field",
                    }],
                })(
                    <Select onSelect={(action) => setStateHandler(onSelectAction(action))}
                            placeholder="The next step after this block">{
                        blockOptions.actions.map((action, i) =>
                            <Option key={i}
                                    value={action}>{action}</Option>)
                    }</Select>
                )
                : <Spin><Select placeholder="The next step after this block"></Select></Spin>
        }
    </FormItem>
);

export const ShowGoToBlockFormItem = ({FormItem, layout, getFieldDecorator, allBlocks, showGoToBlock, block}) => {
    return (
        showGoToBlock ?
            (
                <FormItem label="Go To Specific Block" {...layout}>
                    {console.log(block.content.blockToGoID)}
                    {
                        getFieldDecorator('blockToGoID',
                            {
                                initialValue: block.content.blockToGoID ? block.content.blockToGoID : undefined,
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
                </FormItem>
            ) : null
    );
};

export const ShowGoToGroupFormItem = ({FormItem, layout, getFieldDecorator, allGroups, showGoToGroup}) => {
    return (
        showGoToGroup ?
            (
                <FormItem label="Go To Specific Group"
                          extra="The selected group will start from its first block"
                          {...layout}>
                    {
                        getFieldDecorator('blockToGoIDGroup',
                            {
                                initialValue: this.state.groupName ? this.state.groupName : undefined,
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
                </FormItem>
            ) : null
    );
};

export const ButtonsForm = (handleNewBlock, handleEditBlock, handleDeleteBlock, onSubmit, block) => (
    handleNewBlock ? [
        <Button key="cancel" onClick={() => onCancel(handleNewBlock, handleEditBlock)}>Cancel</Button>,
        <Button key="submit" type="primary" onClick={onSubmit}>Add</Button>
    ] : [
        <Button key="delete" type="danger"
                onClick={() => onDelete(block.id, block.type, handleDeleteBlock)}>
            Delete
        </Button>,
        <Button key="cancel" onClick={() => onCancel(handleNewBlock, handleEditBlock)}>Cancel</Button>,
        <Button key="submit" type="primary" onClick={onSubmit}>Update</Button>
    ]
);
