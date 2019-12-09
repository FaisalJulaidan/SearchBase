import { Button, Cascader, Checkbox, Input, Select, Spin } from 'antd';
import React from 'react';
import { onCancel, onSelectAction } from '../CardTypesHelpers';

const Option = Select.Option;
const CheckboxGroup = Checkbox.Group;

// Common Components
export const QuestionFormItem = ({ FormItem, layout, getFieldDecorator, block, placeholder }) => {
    return (
        <FormItem label="Question"
                  extra="The above text will be shown in a bubble inside the chat"
                  {...layout}>
            {getFieldDecorator('text', {
                initialValue: block.Content.text,
                rules: [{
                    required: true,
                    message: 'Please input a question'
                }]
            })(
                <Input placeholder={placeholder}/>
            )}
        </FormItem>
    );
};

export const DataTypeFormItem = ({ FormItem, layout, getFieldDecorator, options, block, blockType }) => {
    // This will create the Cascader content and will put every userType's associated dataType in a category
    const dataTypesMenu = [];
    const dataTypesFiltered = options.flow.dataTypes.filter(dt => dt.blockTypes.includes(blockType));
    options.flow.dataTypeSections.forEach((dts, i) => {
        dataTypesMenu[i] = {
            value: dts,
            label: dts,
            children: dataTypesFiltered
                .filter(dt => dt.dataTypeSection === dts && dt.dataTypeSection !== 'No Type')
                .map(dt => {
                    return { value: dt.name, label: dt.name };
                })
        };
    });

    // Define initial value. Because cascader only accepts array as initial value we need to create one
    let initialValue = [block.DataType?.dataTypeSection, block.DataType?.name];
    if (!(initialValue[0])) initialValue = [];


    return (
        <FormItem label="Data Type" {...layout}
                  extra="Selecting a Data Type will result in a smarter AI processing and accurate data collection. Each question type has its unique Data Types list">
            {

                getFieldDecorator('dataType', {
                    initialValue: initialValue,
                    rules: [{ type: 'array', required: true, message: 'Please specify the data type!' }]
                })(
                    <Cascader
                        options={dataTypesMenu.filter(item => item.children.length > 0 || item.value === 'No Type')}/>
                )
            }
        </FormItem>
    );
};

//TODO: Needs to be checked
export const StoreInDBFormItem = ({ FormItem, layout, getFieldDecorator, block, blockOptions }) => (
    <FormItem label="Store responses?" {...layout}>
        {getFieldDecorator('storeInDB', {
            valuePropName: 'checked',
            initialValue: block.alwaysStoreInDB ? block.alwaysStoreInDB : true
        })(
            <Checkbox disabled={blockOptions.alwaysStoreInDB}>
                Users' responses should be recorded</Checkbox>
        )}
    </FormItem>
);

export const AfterMessageFormItem = ({ FormItem, layout, getFieldDecorator, block, fieldName }) => (
    <FormItem label="After message"
              extra="This message will display straight after the user's response"
              {...layout}>
        {getFieldDecorator(fieldName || 'afterMessage', {
            initialValue: block.Content.afterMessage ? block.Content.afterMessage : undefined,
            rules: [{
                required: false,
                message: 'Please input question field'
            }]
        })(
            <Input placeholder="Ex: Your input is recorded"/>
        )}
    </FormItem>
);

export const ActionFormItem = ({ FormItem, layout, getFieldDecorator, setStateHandler, blockOptions, block, fieldName }) => (
    <FormItem label="Action" {...layout}>
        {
            blockOptions.actions ?
                getFieldDecorator(fieldName || 'action', {
                    initialValue: block.Content.action ? block.Content.action : undefined,
                    rules: [{
                        required: true,
                        message: 'Please select an action'
                    }]
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

export const ShowGoToBlockFormItem = ({ FormItem, layout, getFieldDecorator, allBlocks, showGoToBlock, block, fieldName }) => {
    let currentBlock = block;
    return (
        showGoToBlock ?
            (
                <FormItem label="Go To Specific Block" {...layout}>
                    {
                        getFieldDecorator(fieldName || 'blockToGoID',
                            {
                                initialValue: currentBlock.Content.blockToGoID ? currentBlock.Content.blockToGoID : undefined,
                                rules: [{ required: true, message: 'Please select your next block' }]
                            }
                        )(
                            <Select placeholder="The next block to go to">{
                                allBlocks.map((block, i) => {
                                    if (block.ID !== currentBlock.ID)
                                        return <Option key={i} value={block.ID}>
                                            {`(${block.Type}) ${block.Content.text ? block.Content.text : ''}`}
                                        </Option>;
                                })
                            }</Select>
                        )
                    }
                </FormItem>
            ) : null
    );
};

export const ShowGoToGroupFormItem = ({ FormItem, layout, getFieldDecorator, block, currentGroup, allGroups, showGoToGroup, fieldName }) => {
    allGroups = allGroups.filter(group => group.id !== currentGroup.id);
    const selectedGroup = allGroups.find(group => !!group.blocks.find(groupBlock => block.Content?.blockToGoID === groupBlock.ID));

    return (
        showGoToGroup ?
            (
                <FormItem label="Go To Specific Group"
                          extra="The selected group will start from its first block"
                          {...layout}>
                    {
                        getFieldDecorator(fieldName || 'blockToGoIDGroup',
                            {
                                initialValue: block && selectedGroup ? selectedGroup.blocks[0].ID : undefined,
                                rules: [{ required: true, message: 'Please select your next group' }]
                            }
                        )(
                            <Select placeholder="The first next block of a group">
                                {
                                    allGroups.map((group, i) => {
                                            if (group.blocks[0]) {
                                                {
                                                    console.log(group.blocks[0].ID);
                                                }
                                                return <Option key={i} value={group.blocks[0].ID}>
                                                    {`${group.name}`}
                                                </Option>;
                                            } else
                                                return <Option disabled key={i} value={group.name}>
                                                    {`${group.name}`}
                                                </Option>;
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
                onClick={() => handleDeleteBlock(block)}>
            Delete
        </Button>,
        <Button key="cancel" onClick={() => onCancel(handleNewBlock, handleEditBlock)}>Cancel</Button>,
        <Button key="submit" type="primary" onClick={() => onSubmit(block)}>Update</Button>
    ];
};


export const FileTypesFormItem = ({ FormItem, block, layout, getFieldDecorator, typesAllowed }) => (
    <FormItem label="File Types" {...layout}>
        {
            typesAllowed ?
                getFieldDecorator('fileTypes', {
                    initialValue: block.Content.fileTypes,
                    rules: [{
                        required: true,
                        message: 'Please select the accepted file type'
                    }]
                })(
                    <CheckboxGroup options={typesAllowed}/>
                )
                : <Spin/>
        }
    </FormItem>
);

export const DatabaseTypeFormItem = ({ FormItem, block, getFieldDecorator, layout, options }) => (
    <FormItem label="Database Type" {...layout}
              extra="All databases of the same selected type (Jobs, Candidate) will be be scanned for solutions">
        {
            getFieldDecorator('databaseType', {
                initialValue: block.Content.databaseType ?
                    options.databases.types.find(type => type === block.Content.databaseType)
                    : undefined,
                rules: [{
                    required: true,
                    message: 'Please select a database type ' +
                        'If you don\'t have one please go to Database section form the left menu and upload one, ' +
                        'otherwise you won\'t be able to creat a Solution block and search for solutions in the chatbot'
                }]
            })(
                <Select placeholder="EX: Jobs">{options.databases.types.map((type, i) =>
                    <Option key={i} value={type}>{type}</Option>)
                }</Select>
            )
        }
    </FormItem>
);

export const ScoreFormItem = ({ FormItem, layout, block, getFieldDecorator }) => (
    <FormItem label="Qualification Points" {...layout}
              extra="The answer with the highest points will weight the most in the candidate's ranking">
        {
            getFieldDecorator('scoreWeight', {
                initialValue: block.Content.score,
                rules: [{
                    required: true,
                    message: 'Please select score '
                }]
            })(
                <Select placeholder="Select score weight">
                    <Option value={5}>5</Option>
                    <Option value={4}>4</Option>
                    <Option value={3}>3</Option>
                    <Option value={2}>2</Option>
                    <Option value={1}>1</Option>
                    <Option value={0}>0</Option>
                    <Option value={-999}>Disqualify Immediately</Option>
                </Select>
            )
        }
    </FormItem>
);
