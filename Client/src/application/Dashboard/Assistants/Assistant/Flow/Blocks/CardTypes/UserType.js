import React, { Component } from 'react';
import { Card, Checkbox, Divider, Form, Input, Select } from 'antd';

import { getInitialVariables, initActionType, initActionTypeSkip, onSelectAction } from './CardTypesHelpers';
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

class UserType extends Component {

    state = {
        errors: {}
    };

    componentDidMount() {
        const { modalState, options } = this.props;
        const { block } = getInitialVariables(options.flow, modalState);
        this.setState({
            ...initActionType(block, this.props.modalState.allGroups),
            ...initActionTypeSkip(block, this.props.modalState.allGroups),
            showSkip: block.Skippable || false,
            tags: block.Content.keywords || []
        }, () => {
            const { blockOptions } = getInitialVariables(options.flow, modalState, 'User Type');
            const UserTypesState = {};

            for (const type of blockOptions.types) {
                UserTypesState[type] = {
                    checked: !!this.getUserType(type, 'value'),
                    value: type,
                    text: this.getUserType(type, 'text'),
                    score: this.getUserType(type, 'score'),
                    action: this.getUserType(type, `action`),
                    showGoToBlock: onSelectAction(this.getUserType(type, `action`)).showGoToBlock,
                    showGoToGroup: onSelectAction(this.getUserType(type, `action`)).showGoToGroup
                };
            }

            const UserTypesErrors = {};
            for (const type of blockOptions.types) {
                UserTypesErrors[type] = {
                    text: false,
                    score: false
                };
            }

            this.setState({
                UserTypesState,
                errors: UserTypesErrors,
                hasChecked: true
            });
        });
    }

    validateCustomFormItems = () => {
        // prepare the types objects to be sent to the server
        const UserTypesState = { ...this.state.UserTypesState };

        Object.keys(UserTypesState).map(key => {
            if (!UserTypesState[key].checked)
                return delete UserTypesState[key];

            if (!UserTypesState[key].text)
                this.setState(state => state.errors[key].text = true);
            else
                this.setState(state => state.errors[key].text = false);

            if (!UserTypesState[key].score)
                this.setState(state => state.errors[key].score = true);
            else
                this.setState(state => state.errors[key].score = false);
        });
    };

    onSubmit = () => this.props.form.validateFields((err, values) => {

        const flowOptions = this.props.options.flow;

        // prepare the types objects to be sent to the server
        const UserTypesState = { ...this.state.UserTypesState };

        this.validateCustomFormItems();

        let UserTypesErrors = { ...this.state.errors };
        UserTypesErrors = Object.keys(UserTypesErrors).reduce((r, k) => r.concat(UserTypesErrors[k]), []);
        UserTypesErrors = UserTypesErrors.map(item => Object.keys(item).reduce((r, k) => r.concat(item[k]), [])).flat();

        const hasErr = UserTypesErrors.includes(true);
        const hasChecked = Object.keys(UserTypesState).reduce((r, k) => r.concat(UserTypesState[k].checked), []).includes(true);

        if (!hasChecked) {
            return this.setState({ hasChecked: false });
        }

        if (!err && !hasErr) {
            const types = [];
            Object.keys(UserTypesState).map(key => {

                if (!UserTypesState[key].checked)
                    return delete UserTypesState[key];

                delete UserTypesState[key].checked;
                delete UserTypesState[key].showGoToBlock;
                delete UserTypesState[key].showGoToGroup;

                UserTypesState[key] = {
                    ...UserTypesState[key],
                    blockToGoID: values[`${key}_blockToGoID`] || values[`${key}_blockToGoIDGroup`] || null,
                    action: values[`${key}_action`],
                    afterMessage: values[`${key}_afterMessage`] || ''
                };

                types.push({ ...UserTypesState[key] });
            });


            let options = {
                Type: 'User Type',
                StoreInDB: false,

                DataType: flowOptions.dataTypes.find((dataType) => dataType.name === 'User Type'),

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


    getUserType = (type, attr) => {
        const { modalState, options } = this.props;
        const { block } = getInitialVariables(options.flow, modalState, 'User Type');
        let value = block.Content.types &&
            block.Content.types.find(x => x.value === type) &&
            block.Content.types.find(x => x.value === type)[attr];
        if (value === 0 || value)
            return value;
        else
            return undefined;
    };


    componentWillMount() {
        const { modalState, options } = this.props;
        const { block } = getInitialVariables(options.flow, modalState);
        this.setState(initActionType(block, this.props.modalState.allGroups));
    }


    render() {
        const { modalState, options, form, handleNewBlock, handleEditBlock, handleDeleteBlock } = this.props;
        const { blockOptions, block } = getInitialVariables(options.flow, modalState, 'User Type');
        const { allGroups, allBlocks, currentGroup, layout } = modalState;
        const { getFieldDecorator } = form;
        const { showSkip, UserTypesState } = this.state;

        const buttons = ButtonsForm(handleNewBlock, handleEditBlock, handleDeleteBlock, this.onSubmit, block);
        console.log(this.getUserType('Client', 'score'));
        return (
            <Card style={{ width: '100%' }} actions={buttons}>
                <Form layout='horizontal'>


                    <QuestionFormItem FormItem={FormItem} block={block}
                                      getFieldDecorator={getFieldDecorator}
                                      layout={layout}
                                      placeholder="Ex: What best describes you?"/>

                    <Divider dashed={true} style={{ fontWeight: 'normal', fontSize: '14px' }}>
                        User Types
                    </Divider>

                    {
                        blockOptions.types.map(
                            (type, i) =>
                                <div key={i}>
                                    <div className={styles.PredefinedValues}>
                                        <div className={
                                            [
                                                !this.state.hasChecked && 'has-error',
                                                'ant-col ant-col-6 ant-form-item-label'
                                            ].join(' ')
                                        }>
                                            <Checkbox className={styles.CheckBox}
                                                      defaultChecked={!!this.getUserType(type, 'value')}
                                                      onChange={e => {
                                                          this.setState(state => {
                                                              state.UserTypesState[type].checked = e.target.checked;
                                                              state.hasChecked = true;

                                                              if (!e.target.checked)
                                                                  state.errors[type] = {
                                                                      text: false,
                                                                      score: false
                                                                  };

                                                              return state;
                                                          });
                                                      }}>
                                                {type}
                                            </Checkbox>
                                            {
                                                !this.state.hasChecked &&
                                                <div className="ant-form-explain">Please Select one</div>
                                            }
                                        </div>

                                        <div className={
                                            [
                                                styles.Inputs,
                                                'ant-col ant-col-14 ant-form-item-control-wrapper'
                                            ].join(' ')
                                        }>

                                            <div
                                                className={[this.state.errors[type]?.text && 'has-error', styles.Text].join(' ')}>
                                                <Input disabled={UserTypesState && !UserTypesState[type].checked}
                                                       onChange={e => {
                                                           const val = e.target.value;
                                                           this.setState(state => {
                                                                   state.UserTypesState[type].text = val;
                                                                   return state;
                                                               },
                                                               () => this.validateCustomFormItems());
                                                       }}
                                                       defaultValue={block.Content.types && block.Content.types.find(x => x.value === type)?.text || undefined}
                                                       placeholder={type}/>
                                                {
                                                    this.state.errors[type]?.text &&
                                                    <div className="ant-form-explain">Please add text</div>
                                                }
                                            </div>

                                            <div
                                                className={[this.state.errors[type]?.score && 'has-error', styles.Score].join(' ')}>
                                                <Select disabled={UserTypesState && !UserTypesState[type].checked}
                                                        placeholder="Select score weight"
                                                        defaultValue={this.getUserType(type, 'score')}
                                                        onChange={value => {
                                                            this.setState(state => state.UserTypesState[type].score = value,
                                                                () => this.validateCustomFormItems());
                                                        }}>
                                                    <Option value={5}>5</Option>
                                                    <Option value={4}>4</Option>
                                                    <Option value={3}>3</Option>
                                                    <Option value={2}>2</Option>
                                                    <Option value={1}>1</Option>
                                                    <Option value={0}>0</Option>
                                                    <Option value={-999}>Disqualify Immediately</Option>
                                                </Select>
                                                {
                                                    this.state.errors[type]?.score &&
                                                    <div className="ant-form-explain">Please select a score</div>
                                                }

                                            </div>

                                        </div>

                                    </div>

                                    {UserTypesState && UserTypesState[type].checked &&

                                    <div>
                                        <ActionFormItem FormItem={FormItem}
                                                        blockOptions={blockOptions}
                                                        block={{
                                                            Content: {
                                                                ID: block.ID,
                                                                action: this.getUserType(type, 'action')
                                                            }
                                                        }}
                                                        setStateHandler={(showActions) => {
                                                            UserTypesState[type].showGoToBlock = showActions.showGoToBlock;
                                                            UserTypesState[type].showGoToGroup = showActions.showGoToGroup;
                                                            this.setState({ ...UserTypesState });
                                                        }}
                                                        getFieldDecorator={getFieldDecorator}
                                                        layout={layout}
                                                        fieldName={`${type}_action`}/>

                                        <ShowGoToBlockFormItem FormItem={FormItem}
                                                               block={{
                                                                   ID: block.ID,
                                                                   Content: {
                                                                       blockToGoID: this.getUserType(type, 'blockToGoID')
                                                                   }
                                                               }}
                                                               allBlocks={allBlocks}
                                                               showGoToBlock={UserTypesState[type].showGoToBlock}
                                                               getFieldDecorator={getFieldDecorator}
                                                               layout={layout}
                                                               fieldName={`${type}_blockToGoID`}/>

                                        <ShowGoToGroupFormItem FormItem={FormItem}
                                                               block={{
                                                                   ID: block.ID,
                                                                   Content: {
                                                                       blockToGoID: this.getUserType(type, 'blockToGoID')
                                                                   }
                                                               }}
                                                               allGroups={allGroups}
                                                               currentGroup={currentGroup}
                                                               showGoToGroup={UserTypesState[type].showGoToGroup}
                                                               getFieldDecorator={getFieldDecorator}
                                                               layout={layout}
                                                               fieldName={`${type}_blockToGoIDGroup`}/>

                                        <AfterMessageFormItem FormItem={FormItem}
                                                              block={{
                                                                  ID: block.ID,
                                                                  Content: {
                                                                      afterMessage: this.getUserType(type, 'afterMessage')
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

export default Form.create()(UserType);

