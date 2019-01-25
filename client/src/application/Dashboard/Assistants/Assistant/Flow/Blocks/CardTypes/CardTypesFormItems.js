import {Button, Checkbox, Input, Select, Spin} from "antd";
import React from 'react';
import {onCancel, onDelete, onSelectAction} from "./CardTypesHelpers";

const Option = Select.Option;

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

export const SkippableFormItem = ({FormItem, layout, getFieldDecorator, block}) => (
    <FormItem label="Skippable?" {...layout}>
        {getFieldDecorator('isSkippable', {
            valuePropName: 'checked',
            initialValue: block.isSkippable || false,
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
            initialValue: block.content.afterMessage,
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
                    initialValue: block.content.action,
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
