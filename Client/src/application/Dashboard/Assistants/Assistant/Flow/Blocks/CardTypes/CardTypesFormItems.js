import {Button, Cascader, Checkbox, Input, Select, Spin,} from "antd";
import React from 'react';
import {onCancel, onSelectAction} from "./CardTypesHelpers";

const Option = Select.Option;
const CheckboxGroup = Checkbox.Group;
const {TextArea} = Input;

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
    if (!(initialValue[0])) initialValue = ['No Type'];


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

export const SkippableFormItem = ({FormItem, layout, getFieldDecorator, block, setStateHandler, label = 'Skippable', toShow = false}) => (
    <FormItem label={label} {...layout}
              extra={'When this is checked users can skip responding'}>
        {getFieldDecorator('isSkippable', {
            valuePropName: 'checked',
            initialValue: block.Skippable ? block.Skippable : toShow,
        })(
            <Checkbox onChange={(event) => setStateHandler ? setStateHandler({showSkip: event.target.checked}) : null}>
                Users can skip answering this question
            </Checkbox>
        )}
    </FormItem>
);

//TODO: Needs to be checked
export const StoreInDBFormItem = ({FormItem, layout, getFieldDecorator, block, blockOptions}) => (
    <FormItem label="Store responses?" {...layout}>
        {getFieldDecorator('storeInDB', {
            valuePropName: 'checked',
            initialValue: block.alwaysStoreInDB ? block.alwaysStoreInDB : true,
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

export const RawTextFormItem = ({FormItem, layout, getFieldDecorator, block, placeholder}) => (
    <FormItem label="Raw Text"
              extra="This message will displayed straight after the previous block"
              {...layout}>
        {getFieldDecorator('rawText', {
            initialValue: block.Content.text ? block.Content.text : undefined,
            rules: [{
                required: true,
                message: "Please input raw text field",
            }],
        })(
            <TextArea placeholder={placeholder} autosize={{minRows: 2, maxRows: 6}}/>
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
    let currentBlock = block;
    return (
        showGoToBlock ?
            (
                <FormItem label="Go To Specific Block" {...layout}>
                    {
                        getFieldDecorator('blockToGoID',
                            {
                                initialValue: currentBlock.Content.blockToGoID ? currentBlock.Content.blockToGoID : undefined,
                                rules: [{required: true, message: "Please select your next block"}]
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

export const ShowGoToGroupFormItem = ({FormItem, layout, getFieldDecorator, block, currentGroup, allGroups, showGoToGroup}) => {
    allGroups = allGroups.filter(group => group.id !== currentGroup.id);
    const selectedGroup = allGroups.find(group => !!group.blocks.find(groupBlock => block.Content?.blockToGoID === groupBlock.ID));

    return (
        showGoToGroup ?
            (
                <FormItem label="Go To Specific Group"
                          extra="The selected group will start from its first block"
                          {...layout}>
                    {
                        getFieldDecorator('blockToGoIDGroup',
                            {
                                initialValue: block && selectedGroup ? selectedGroup.blocks[0].ID : undefined,
                                rules: [{required: true, message: "Please select your next group"}]
                            }
                        )(
                            <Select placeholder="The first next block of a group">
                                {
                                allGroups.map((group, i) => {
                                    if (group.blocks[0]) {
                                        {console.log(group.blocks[0].ID)}
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

// Skip Section
//////////////////////////////////////////////////

export const SkipTextFormItem = ({FormItem, layout, getFieldDecorator, block, text = 'Skip!'}) => {
    return (
        <FormItem label="Button Text"
                  extra="The above text will be shown in a button"
                  {...layout}>
            {getFieldDecorator('SkipText', {
                initialValue: block.SkipText || text,
                rules: [{
                    required: true,
                    max: 37,
                    message: "Text it should not exceed 37 character",
                }],
            })(
                <Input/>
            )}
        </FormItem>
    )
};

export const SkipFormItem = ({FormItem, layout, getFieldDecorator, setStateHandler, blockOptions, block, label = 'Skip Action'}) => {
    return <FormItem label={label} {...layout}>
        {
            blockOptions.actions ?
                getFieldDecorator('SkipAction', {
                    initialValue: block.SkipAction ? block.SkipAction : undefined,
                    rules: [{
                        required: true,
                        message: "Please select an action",
                    }],
                })(
                    <Select onSelect={(action) => setStateHandler(onSelectAction(action, true))}
                            placeholder="The next step after this block">{
                        blockOptions.actions.map((action, i) =>
                            <Option key={i} value={action}>{action}</Option>)
                    }</Select>
                )
                : <Spin><Select placeholder="The next step after this block"></Select></Spin>
        }
    </FormItem>
};

export const ShowGoToBlockSkipFormItem = ({FormItem, layout, getFieldDecorator, allBlocks, showGoToBlock, block}) => {
    let currentBlock = block;
    return (
        showGoToBlock ?
            (
                <FormItem label="Go To Specific Block"
                          extra="The selected block will be shown after clicking on 'Not Interested' button"
                          {...layout}>
                    {
                        getFieldDecorator('skipBlockToGoID',
                            {
                                initialValue: currentBlock.SkipBlockToGoID ? currentBlock.SkipBlockToGoID : undefined,
                                rules: [{required: true, message: "Please select your next block"}]
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

export const ShowGoToGroupSkipFormItem = ({FormItem, layout, getFieldDecorator, block, currentGroup, allGroups, showGoToGroup}) => {
    allGroups = allGroups.filter(group => group.id !== currentGroup.id);
    const selectedGroup = allGroups.find(group => !!group.blocks.find(groupBlock => block.SkipBlockToGoID === groupBlock?.ID));
    return (
        showGoToGroup ?
            (
                <FormItem label="Go To Specific Group"
                          extra="The selected group will start from its first block"
                          {...layout}>
                    {
                        getFieldDecorator('skipBlockToGoIDGroup',
                            {
                                initialValue: block && selectedGroup ? selectedGroup.blocks[0].ID : undefined,
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
                onClick={() => handleDeleteBlock(block)}>
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

export const ScoreFormItem = ({FormItem, layout, block, getFieldDecorator}) => (
    <FormItem label="Qualification Points" {...layout}
              extra="The answer with the highest points will weight the most in the candidate's ranking">
        {
            getFieldDecorator('scoreWeight', {
                initialValue: block.Content.score,
                rules: [{
                    required: true,
                    message: "Please select score "
                }],
            })(
                <Select placeholder="Select score weight">
                    <Option value={5}>5</Option>
                    <Option value={4}>4</Option>
                    <Option value={3}>3</Option>
                    <Option value={2}>2</Option>
                    <Option value={1}>1</Option>
                    <Option value={-999}>Disqualify Immediately</Option>
                </Select>
            )
        }
    </FormItem>
);
