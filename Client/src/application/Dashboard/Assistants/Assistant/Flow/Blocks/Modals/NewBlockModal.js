import React, { Component } from 'react';
import styles from '../Blocks.module.less';

import { Icon, Modal, Tabs } from 'antd';

import UserInput from '../CardTypes/UserInput';
import Question from '../CardTypes/Question';
import FileUpload from '../CardTypes/FileUpload';
import Solutions from '../CardTypes/Solutions';
import RawText from '../CardTypes/RawText';
import SalaryPicker from '../CardTypes/SalaryPicker';
import JobType from '../CardTypes/JobType';
import UserType from '../CardTypes/UserType';
import DatePicker from '../CardTypes/DatePicker';

const TabPane = Tabs.TabPane;
const MyModal = Modal;

class NewBlockModal extends Component {

    state = {
        layout: {
            labelCol: { span: 6 },
            wrapperCol: { span: 14 }
        },
        allBlocks: [],
        allGroups: [],
        currentGroup: null,
        block: null
    };

    componentWillReceiveProps(nextProps) {
        this.setState({
            allBlocks: nextProps.allBlocks,
            allGroups: nextProps.allGroups,
            currentGroup: nextProps.currentGroup
        });
    }

    handleNewBlock = (newBlock) => {
        if (newBlock)
            this.props.handleAddBlock(newBlock);
        this.props.closeModal();
    };

    onChangeTab = (currentTab) => this.setState({ currentTab });

    render() {
        return (
            <div>
                <MyModal className={styles.NewBlockModal}
                         title="Add New Question"
                         visible={this.props.visible}
                         onCancel={this.props.closeModal}
                         destroyOnClose={true}
                         footer={null}>

                    <Tabs type="card"
                          tabPosition={'right'}
                          defaultActiveKey={'Question'}
                          onChange={this.onChangeTab}>

                        <TabPane tab={<span><Icon type="question-circle"/>Pre-Selected Answers</span>}
                                 key="Question">
                            <Question modalState={this.state}
                                      handleNewBlock={this.handleNewBlock}
                                      options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="form"/>Open Answer</span>}
                                 key="UserInput">
                            <UserInput modalState={this.state}
                                       addNewDataCategory={this.showNewDataCategoryModal}
                                       handleNewBlock={this.handleNewBlock}
                                       options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="contacts"/>User Type</span>} key="UserType">
                            <UserType modalState={this.state}
                                      handleNewBlock={this.handleNewBlock}
                                      options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="solution"/>Job Type</span>} key="JobType">
                            <JobType modalState={this.state}
                                     handleNewBlock={this.handleNewBlock}
                                     options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="dollar"/>Salary Picker</span>}
                                 key="SalaryPicker">
                            <SalaryPicker modalState={this.state}
                                          handleNewBlock={this.handleNewBlock}
                                          options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="calendar"/>Date Picker</span>} key="DatePicker">
                            <DatePicker modalState={this.state}
                                        handleNewBlock={this.handleNewBlock}
                                        options={this.props.options}/>
                        </TabPane>


                        <TabPane tab={<span><Icon type="file-add"/>File Upload</span>}
                                 key="FileUpload">
                            <FileUpload modalState={this.state}
                                        handleNewBlock={this.handleNewBlock}
                                        options={this.props.options}/>
                        </TabPane>


                        <TabPane tab={<span><Icon type="font-size"/>Raw Text</span>}
                                 key="RawText">
                            <RawText modalState={this.state}
                                     handleNewBlock={this.handleNewBlock}
                                     options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="tag"/>Data Scan and Return</span>}
                                 key="Solutions">
                            <Solutions modalState={this.state}
                                       handleNewBlock={this.handleNewBlock}
                                       options={this.props.options}/>
                        </TabPane>
                    </Tabs>
                </MyModal>


            </div>


        );
    }
}


export default NewBlockModal;
