import { Checkbox, Input, Select, Spin } from 'antd';
import React from 'react';
import { onSelectAction } from '../CardTypesHelpers';

const Option = Select.Option;

// Skip Section
//////////////////////////////////////////////////

export const SkippableFormItem = ({ FormItem, layout, getFieldDecorator, block, setStateHandler, label = 'Skippable', toShow = false }) => (
    <FormItem label={label} {...layout}
              extra={'When this is checked users can skip responding'}>
        {getFieldDecorator('isSkippable', {
            valuePropName: 'checked',
            initialValue: block.Skippable ? block.Skippable : toShow
        })(
            <Checkbox
                onChange={(event) => setStateHandler ? setStateHandler({ showSkip: event.target.checked }) : null}>
                Users can skip answering this question
            </Checkbox>
        )}
    </FormItem>
);

export const SkipTextFormItem = ({ FormItem, layout, getFieldDecorator, block, text = 'Skip!' }) => {
    return (
        <FormItem label="Button Text"
                  extra="The above text will be shown in a button"
                  {...layout}>
            {getFieldDecorator('SkipText', {
                initialValue: block.SkipText || text,
                rules: [{
                    required: true,
                    max: 37,
                    message: 'Text it should not exceed 37 character'
                }]
            })(
                <Input/>
            )}
        </FormItem>
    );
};

export const SkipFormItem = ({ FormItem, layout, getFieldDecorator, setStateHandler, blockOptions, block, label = 'Skip Action' }) => {
    return <FormItem label={label} {...layout}>
        {
            blockOptions.actions ?
                getFieldDecorator('SkipAction', {
                    initialValue: block.SkipAction ? block.SkipAction : undefined,
                    rules: [{
                        required: true,
                        message: 'Please select an action'
                    }]
                })(
                    <Select onSelect={(action) => setStateHandler(onSelectAction(action, true))}
                            placeholder="The next step after this block">{
                        blockOptions.actions.map((action, i) =>
                            <Option key={i} value={action}>{action}</Option>)
                    }</Select>
                )
                : <Spin><Select placeholder="The next step after this block"></Select></Spin>
        }
    </FormItem>;
};

export const ShowGoToBlockSkipFormItem = ({ FormItem, layout, getFieldDecorator, allBlocks, showGoToBlock, block }) => {
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

export const ShowGoToGroupSkipFormItem = ({ FormItem, layout, getFieldDecorator, block, currentGroup, allGroups, showGoToGroup }) => {
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
                                rules: [{ required: true, message: 'Please select your next group' }]
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
