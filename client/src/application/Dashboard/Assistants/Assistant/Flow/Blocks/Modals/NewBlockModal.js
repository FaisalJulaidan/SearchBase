import React, {Component} from 'react';


import {Icon, Modal, Tabs} from 'antd';

import UserInput from "../CardTypes/UserInput";
import Question from "../CardTypes/Question";
import FileUpload from "../CardTypes/FileUpload";
import Solutions from "../CardTypes/Solutions";
import RawText from "../CardTypes/RawText";

const TabPane = Tabs.TabPane;
const MyModal = Modal;
class NewBlockModal extends Component {

    state = {
        layout: {
            labelCol: {span: 6},
            wrapperCol: {span: 14}
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
            currentGroup: nextProps.currentGroup,
        })
    }

    handleNewBlock = (newBlock) => {
        if (newBlock)
            this.props.handleAddBlock(newBlock);
        this.props.closeEditAutoPilotModal();
    };

    onChangeTab = (currentTab) => this.setState({currentTab});

    render() {
        return (
            <div>
                <MyModal width={800}
                         title="Add New Question"
                         visible={this.props.newAutoPilotModalVisible}
                         onCancel={this.props.closeEditAutoPilotModal}
                         destroyOnClose={true}
                         footer={null}>

                    <Tabs type="card" onChange={this.onChangeTab}>

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

                        <TabPane tab={<span><Icon type="file-add"/>File Upload</span>}
                                 key="FileUpload">
                            <FileUpload modalState={this.state}
                                        handleNewBlock={this.handleNewBlock}
                                        options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="tag"/>Data Scan and Return</span>}
                                 key="Solutions">
                            <Solutions modalState={this.state}
                                       handleNewBlock={this.handleNewBlock}
                                       options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="font-size"/>Raw Text</span>}
                                 key="RawText">
                            <RawText modalState={this.state}
                                     handleNewBlock={this.handleNewBlock}
                                     options={this.props.options}/>
                        </TabPane>

                    </Tabs>
                </MyModal>


            </div>



        );
    }
}


export default NewBlockModal
