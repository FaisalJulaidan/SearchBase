import React, { Component } from 'react';
import { Card, Checkbox, Divider, Form, Input, Select } from 'antd';

import { getInitialVariables, initActionType, initActionTypeSkip } from './CardTypesHelpers';
import {
    ActionFormItem,
    AfterMessageFormItem,
    ButtonsForm,
    QuestionFormItem,
    ShowGoToBlockFormItem,
    ShowGoToBlockSkipFormItem,
    ShowGoToGroupFormItem,
    ShowGoToGroupSkipFormItem,
    SkipFormItem,
    SkippableFormItem,
    SkipTextFormItem
} from './FormItems';
import styles from '../Blocks.module.less';

const FormItem = Form.Item;
const Option = Select.Option;

class JobType extends Component {

    state = {
        showGoToBlock: false,
        showGoToGroup: false,
        errors: {}
    };

    onSubmit = () => this.props.form.validateFields((err, values) => {

        const flowOptions = this.props.options.flow;

        // prepare the objects to be sent to the server
        const jobTypesState = { ...this.state.jobTypesState };

        Object.keys(jobTypesState).map(key => {
            if (!jobTypesState[key].checked)
                delete jobTypesState[key];
        });

        const validateCustomInputs = () => (
            Object.keys(jobTypesState).map(key => {
                if (!jobTypesState[key].text)
                    this.setState(state => state.errors[key].text = true);
                else
                    this.setState(state => state.errors[key].text = false);

                if (!jobTypesState[key].score)
                    this.setState(state => state.errors[key].score = true);
                else
                    this.setState(state => state.errors[key].score = false);
            })
        );

        if (!err) {
            const types = [];
            Object.keys(jobTypesState).map(key => {
                delete jobTypesState[key].checked;
                jobTypesState[key] = {
                    ...jobTypesState[key],
                    blockToGoID: values[`${key}_blockToGoID`] || values[`${key}_blockToGoIDGroup`] || null,
                    action: values[`${key}_action`],
                    afterMessage: values[`${key}_afterMessage`] || ''
                };

                types.push({ ...jobTypesState[key] });
            });

            console.log(types);

            let options = {
                Type: 'Job Type',
                StoreInDB: false,

                DataType: flowOptions.dataTypes.find((dataType) => dataType.name === 'Job Salary'),

                Skippable: values.isSkippable || false,
                SkipText: values.SkipText || 'Skip!',
                SkipAction: values.SkipAction || 'End Chat',
                SkipBlockToGoID: values.skipBlockToGoID || values.skipBlockToGoIDGroup || null,

                Content: {
                    text: values.text,
                    types
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

    componentDidMount() {
        const { modalState, options } = this.props;
        const { block } = getInitialVariables(options.flow, modalState);
        this.setState({
            ...initActionType(block, this.props.modalState.allGroups),
            ...initActionTypeSkip(block, this.props.modalState.allGroups),
            showSkip: block.Skippable || false,
            tags: block.Content.keywords || []
        }, () => {
            const { blockOptions } = getInitialVariables(options.flow, modalState, 'Job Type');
            const jobTypesState = {};
            for (const type of blockOptions.types) {
                jobTypesState[type] = {
                    checked: false,
                    value: type,
                    text: undefined,
                    score: undefined
                };
            }

            const jobTypesErrors = {};
            for (const type of blockOptions.types) {
                jobTypesErrors[type] = {
                    text: false,
                    score: false
                };
            }
            this.setState({ jobTypesState, errors: jobTypesErrors });
        });
    }

    componentWillMount() {
        const { modalState, options } = this.props;
        const { block } = getInitialVariables(options.flow, modalState);
        this.setState(initActionType(block, this.props.modalState.allGroups));
    }


    render() {
        const { modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock } = this.props;
        const { blockOptions, block } = getInitialVariables(options.flow, modalState, 'Job Type');
        const { allGroups, allBlocks, currentGroup, layout } = modalState;
        const { getFieldDecorator } = form;
        const { showSkip, jobTypesState } = this.state;

        const buttons = ButtonsForm(handleNewBlock, handleEditBlock, handleDeleteBlock, this.onSubmit, block);

        return (
            <Card style={{ width: '100%' }} actions={buttons}>
                <Form layout='horizontal'>


                    <QuestionFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={layout}
                                      placeholder="Ex: What is your job?"/>

                    <Divider dashed={true} style={{ fontWeight: 'normal', fontSize: '14px' }}>
                        Job Types
                    </Divider>

                    {
                        blockOptions.types.map(
                            (type, i) =>
                                <div key={i}>
                                    <div className={styles.PredefinedValues}>
                                        <Checkbox className={styles.CheckBox}
                                                  onChange={e => {
                                                      this.setState(state => {
                                                          state.jobTypesState[type].checked = e.target.checked;
                                                          return state;
                                                      });
                                                  }}>
                                            {type}
                                        </Checkbox>

                                        <div className={styles.Inputs}>

                                            <div
                                                className={[this.state.errors[type]?.text && 'has-error', styles.Text].join(' ')}>
                                                <Input disabled={jobTypesState && !jobTypesState[type].checked}
                                                       onChange={e => {
                                                           const val = e.target.value;
                                                           this.setState(state => {
                                                               state.jobTypesState[type].text = val;
                                                               return state;
                                                           });
                                                       }}
                                                       placeholder={type}/>
                                                {
                                                    this.state.errors[type]?.text &&
                                                    <div className="ant-form-explain">Please add text</div>
                                                }
                                            </div>

                                            <div
                                                className={[this.state.errors[type]?.score && 'has-error', styles.Score].join(' ')}>
                                                <Select disabled={jobTypesState && !jobTypesState[type].checked}
                                                        placeholder="Select score weight"
                                                        onChange={value => this.setState(state => state.jobTypesState[type].score = value)}>
                                                    <Option value={5}>5</Option>
                                                    <Option value={4}>4</Option>
                                                    <Option value={3}>3</Option>
                                                    <Option value={2}>2</Option>
                                                    <Option value={1}>1</Option>
                                                    <Option value={-999}>Disqualify Immediately</Option>
                                                </Select>
                                                {
                                                    this.state.errors[type]?.score &&
                                                    <div className="ant-form-explain">Please select a score</div>
                                                }

                                            </div>

                                        </div>

                                    </div>

                                    {jobTypesState && jobTypesState[type].checked &&

                                    <div>
                                        <ActionFormItem FormItem={FormItem}
                                                        blockOptions={blockOptions}
                                                        block={{
                                                            Content: {
                                                                ID: block.ID,
                                                                action: this.state.editedAnswer?.action
                                                            }
                                                        }}
                                                        setStateHandler={(state) => this.setState(state)}
                                                        getFieldDecorator={getFieldDecorator}
                                                        layout={layout}
                                                        fieldName={`${type}_action`}/>

                                        <ShowGoToBlockFormItem FormItem={FormItem}
                                                               block={{
                                                                   ID: block.ID,
                                                                   Content: {
                                                                       blockToGoID: this.state.editedAnswer?.blockToGoID
                                                                   }
                                                               }}
                                                               allBlocks={allBlocks}
                                                               showGoToBlock={this.state.showGoToBlock}
                                                               getFieldDecorator={getFieldDecorator}
                                                               layout={layout}
                                                               fieldName={`${type}_blockToGoID`}/>

                                        <ShowGoToGroupFormItem FormItem={FormItem}
                                                               block={{
                                                                   ID: block.ID,
                                                                   Content: {
                                                                       blockToGoID: this.state.editedAnswer?.blockToGoID
                                                                   }
                                                               }}
                                                               allGroups={allGroups}
                                                               currentGroup={currentGroup}
                                                               showGoToGroup={this.state.showGoToGroup}
                                                               getFieldDecorator={getFieldDecorator}
                                                               layout={layout}
                                                               fieldName={`${type}_blockToGoIDGroup`}/>

                                        <AfterMessageFormItem FormItem={FormItem}
                                                              block={{
                                                                  ID: block.ID,
                                                                  Content: {
                                                                      afterMessage: this.state.editedAnswer?.afterMessage
                                                                  }
                                                              }}
                                                              getFieldDecorator={getFieldDecorator}
                                                              layout={layout}
                                                              fieldName={`${type}_afterMessage`}/>
                                    </div>

                                    }

                                    <Divider/>

                                </div>
                        )
                    }

                    <SkippableFormItem FormItem={FormItem} block={block}
                                       setStateHandler={(state) => this.setState(state)}
                                       getFieldDecorator={getFieldDecorator}
                                       layout={layout}/>
                    {
                        showSkip &&
                        <>
                            <Divider dashed={true} style={{ fontWeight: 'normal', fontSize: '14px' }}>
                                Skip Button
                            </Divider>

                            <SkipTextFormItem FormItem={FormItem}
                                              layout={layout}
                                              getFieldDecorator={getFieldDecorator}
                                              block={block}/>

                            <SkipFormItem FormItem={FormItem}
                                          blockOptions={blockOptions}
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

export default Form.create()(JobType);

