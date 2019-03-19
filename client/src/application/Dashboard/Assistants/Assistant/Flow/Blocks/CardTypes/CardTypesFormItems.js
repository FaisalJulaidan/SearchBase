import {Button, Checkbox, Input, Select, Spin, Cascader} from "antd";
import React from 'react';
import {onCancel, onDelete, onFileTypeChange, onSelectAction} from "./CardTypesHelpers";

const Option = Select.Option;
const CheckboxGroup = Checkbox.Group;

// Common Components
////////////////////////////////////////////
export const QuestionFormItem = ({FormItem, layout, getFieldDecorator, block, placeholder}) => {
    return (
        <FormItem label="Question"
                  extra="The above text will be shown in a bubble inside the chat"
                  {...layout}>
            {getFieldDecorator('text', {
                initialValue: block.Content.text,
                rules: [{
                    required: true,
                    message: "Please input a question",
                }],
            })(
                <Input placeholder={placeholder}/>
            )}
        </FormItem>
    )
};

export const DataTypeFormItem = ({FormItem, layout, getFieldDecorator, options, block}) => {

    // This will create the Cascader content and will put every userType's associated dataType in a category
    const dataTypes = [];
    options.flow.dataTypeSections.forEach((dts, i) => {
        dataTypes[i] = {
            value: dts,
            label: dts,
            children: options.flow.dataTypes
                .filter(dt => dt.dataTypeSection === dts && dt.dataTypeSection !== 'No Type')
                .map(dt => {
                return {value: dt.name, label: dt.name}
            }),
        };
    });

    // Define initial value. Because cascader only accepts array as initial value we need to create one
    let initialValue = [block.DataType?.dataTypeSection, block.DataType?.name];
    if (!(initialValue[0])) initialValue =undefined;


    return (
        <FormItem label="Data Type" {...layout}
                  extra="Selecting a Data Type will result in a smarter AI processing and accurate data collection">
            {

                getFieldDecorator('dataType', {
                    initialValue: initialValue,
                    rules: [{ type: 'array', required: true, message: 'Please specify the data type!' }]
                })(
                    <Cascader options={dataTypes} />
                )
            }
        </FormItem>
    );
};

export const SkippableFormItem = ({FormItem, layout, getFieldDecorator, block}) => (
    <FormItem label="Skippable?" {...layout}>
        {getFieldDecorator('isSkippable', {
            valuePropName: 'checked',
            initialValue: block.Skippable ? block.Skippable : false,
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
                            <Option key={i} value={action}>{action}</Option>)
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

export const ShowGoToGroupFormItem = ({FormItem, layout, getFieldDecorator, currentBlock, currentGroup, allGroups, showGoToGroup}) => {

    allGroups = allGroups.filter(group => group.id !== currentGroup.id);
    const selectedGroup = allGroups.find(group => !!group.blocks.find(block => block.id === currentBlock?.Content?.goToBlockID));

    return (
        showGoToGroup ?
            (
                <FormItem label="Go To Specific Group"
                          extra="The selected group will start from its first block"
                          {...layout}>
                    {
                        getFieldDecorator('blockToGoIDGroup',
                            {
                                initialValue: currentBlock && selectedGroup ? selectedGroup.blocks[0].ID : undefined,
                                rules: [{required: true, message: "Please select your next group"}]
                            }
                        )(
                            <Select placeholder="The first next block of a group">{
                                allGroups.map((group, i) => {
                                    if (group.blocks[0]) {
                                        return <Option key={i} value={group.blocks[0].ID}>
                                                {`${group.name}`}
                                            </Option>;
                                    } else
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
export const ButtonsForm = (handleNewBlock, handleEditBlock, handleDeleteBlock, onSubmit, block) => {
    return handleNewBlock ? [
        <Button key="cancel" onClick={() => onCancel(handleNewBlock, handleEditBlock)}>Cancel</Button>,
        <Button key="submit" type="primary" onClick={() => onSubmit('NewBlock')}>Add</Button>
    ] : [
        <Button key="delete" type="danger"
                onClick={() => onDelete(block.ID, block.Type, handleDeleteBlock)}>
            Delete
        </Button>,
        <Button key="cancel" onClick={() => onCancel(handleNewBlock, handleEditBlock)}>Cancel</Button>,
        <Button key="submit" type="primary" onClick={() => onSubmit(block)}>Update</Button>
    ]
};


export const FileTypesFormItem = ({FormItem, block, layout, getFieldDecorator, typesAllowed}) => (
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
                    <CheckboxGroup options={typesAllowed}/>
                )
                : <Spin/>
        }
    </FormItem>
);

export const DatabaseTypeFormItem = ({FormItem, block, getFieldDecorator, layout, options}) => (
    <FormItem label="Database" {...layout}
              extra="The database to be scanned for solutions (Jobs, Candidate...)">
        {
            getFieldDecorator('databaseType', {
                initialValue: block.Content.databaseType ?
                    options.databases.types.find(type => type === block.Content.databaseType)
                    : undefined,
                rules: [{
                    required: true,
                    message: "Please select a database type " +
                        "If you don't have one please go to Database section form the left menu and upload one, " +
                        "otherwise you won't be able to creat a Solution block and search for solutions in the chatbot",
                }],
            })(
                <Select placeholder="EX: Jobs database">{options.databases.types.map((type, i) =>
                    <Option key={i} value={type}>{type}</Option>)
                }</Select>
            )
        }
    </FormItem>
);