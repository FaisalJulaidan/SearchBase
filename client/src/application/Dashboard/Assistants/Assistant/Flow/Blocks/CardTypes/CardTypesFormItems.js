import {Button, Checkbox, Input, Select, Spin} from "antd";
import React from 'react';
import {onCancel, onDelete, onFileTypeChange, onSelectAction} from "./CardTypesHelpers";

const Option = Select.Option;
const CheckboxGroup = Checkbox.Group;

// Common Components
////////////////////////////////////////////
export const QuestionFormItem = ({FormItem, layout, getFieldDecorator, block, placeholder}) => (
    <FormItem label="Question"
              extra="The above text will be shown in a bubble inside the chat"
              {...layout}>
        {getFieldDecorator('text', {
            initialValue: block.Content.text,
            rules: [{
                required: true,
                message: "Please input question field",
            }],
        })(
            <Input placeholder={placeholder}/>
        )}
    </FormItem>
);

export const DataTypeFormItem = ({FormItem, layout, getFieldDecorator, flowOptions, block}) => (
    <FormItem label="Data Type" {...layout}
              extra="Selecting a Data Type will result in a smarter AI processing and accurate data collection">
        {
            getFieldDecorator('dataType', {
                initialValue: block.DataType ? block.DataType.name : undefined,
                rules: [{
                    required: true,
                    message: "Please specify the data type",
                }]
            })(
                <Select placeholder="Will validate the input and categorise user inputs">
                    {
                        flowOptions.dataTypes.map((type, i) =>
                            <Option key={i} value={type.name}>{type.name}</Option>)
                    }
                </Select>
            )
        }
    </FormItem>
);

export const SkippableFormItem = ({FormItem, layout, getFieldDecorator, block}) => (
    <FormItem label="Skippable?" {...layout}>
        {getFieldDecorator('isSkippable', {
            valuePropName: 'checked',
            initialValue: block.IsSkippable ? block.IsSkippable : undefined,
        })(
            <Checkbox>Users can skip answering this question</Checkbox>
        )}
    </FormItem>
);

//TODO: Needs to be checked
export const StoreInDBFormItem = ({FormItem, layout, getFieldDecorator, block, blockOptions}) => (
    <FormItem label="Store responses?" {...layout}>
        {getFieldDecorator('storeInDB', {
            valuePropName: 'checked',
            initialValue: block.alwaysStoreInDB ? block.alwaysStoreInDB : blockOptions.alwaysStoreInDB,
        })(
            <Checkbox disabled={blockOptions.alwaysStoreInDB}>
                Users' responses should be recorded</Checkbox>
        )}
    </FormItem>
);

export const AfterMessageFormItem = ({FormItem, layout, getFieldDecorator, block}) => (
    <FormItem label="After message"
              extra="This message will display straight after the user's response"
              {...layout}>
        {getFieldDecorator('afterMessage', {
            initialValue: block.Content.afterMessage ? block.Content.afterMessage : undefined,
            rules: [{
                required: false,
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
                    initialValue: block.Content.action ? block.Content.action : undefined,
                    rules: [{
                        required: true,
                        message: "Please select an action",
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
                    {console.log(block.Content.blockToGoID)}
                    {
                        getFieldDecorator('blockToGoID',
                            {
                                initialValue: block.Content.blockToGoID ? block.Content.blockToGoID : undefined,
                                rules: [{required: true, message: "Please select your next block"}]
                            }
                        )(
                            <Select placeholder="The next block to go to">{
                                allBlocks.map((block, i) =>
                                    <Option key={i} value={block.ID}>
                                        {`${block.ID}- (${block.Type}) ${block.Content.text ? block.Content.text : ''}`}
                                    </Option>
                                )
                            }</Select>
                        )
                    }
                </FormItem>
            ) : null
    );
};

export const ShowGoToGroupFormItem = ({FormItem, layout, getFieldDecorator, allGroups, showGoToGroup, groupName}) => {
    return (
        showGoToGroup ?
            (
                <FormItem label="Go To Specific Group"
                          extra="The selected group will start from its first block"
                          {...layout}>
                    {
                        getFieldDecorator('blockToGoIDGroup',
                            {
                                initialValue: groupName ? groupName : undefined,
                                rules: [{required: true, message: "Please select your next group"}]
                            }
                        )(
                            <Select placeholder="The first next block of a group">{
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

// Others
//////////////////////////////////////////////////
export const ButtonsForm = (handleNewBlock, handleEditBlock, handleDeleteBlock, onSubmit, block) => (
    handleNewBlock ? [
        <Button key="cancel" onClick={() => onCancel(handleNewBlock, handleEditBlock)}>Cancel</Button>,
        <Button key="submit" type="primary" onClick={onSubmit}>Add</Button>
    ] : [
        <Button key="delete" type="danger"
                onClick={() => onDelete(block.ID, block.Type, handleDeleteBlock)}>
            Delete
        </Button>,
        <Button key="cancel" onClick={() => onCancel(handleNewBlock, handleEditBlock)}>Cancel</Button>,
        <Button key="submit" type="primary" onClick={onSubmit}>Update</Button>
    ]
);

export const FileTypesFormItem = ({FormItem, layout, getFieldDecorator, typesAllowed, block, setStateHandler}) => (
    <FormItem label="File Types" {...layout}>
        {
            typesAllowed ?
                getFieldDecorator('fileTypes', {
                    initialValue: block.Content.fileTypes,
                    rules: [{
                        required: true,
                        message: "Please select the accepted file type",
                    }]
                })(
                    <CheckboxGroup options={typesAllowed}
                                   onChange={(checkedValues) => setStateHandler(onFileTypeChange(checkedValues))}/>
                )
                : <Spin/>
        }
    </FormItem>
);