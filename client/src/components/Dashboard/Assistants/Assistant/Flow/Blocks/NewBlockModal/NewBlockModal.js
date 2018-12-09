import React, {Component} from 'react';

import {Button, Modal, Icon, Tabs} from 'antd';
import {connect} from "react-redux";

import UserInput from "./Cards/UserInput";
import Question from "./Cards/Question";
import FileUpload from "./Cards/FileUpload";
import Solutions from "./Cards/Solutions";

const TabPane = Tabs.TabPane;

class NewBlockModal extends Component {
    state = {
        beforeAdd: {
            UserInput: false,
            Question: false,
            FileUpload: false,
            Solutions: false
        },
        currentTab: 'UserInput'
    };

    onBeforeAdd = () => {
        switch (this.state.currentTab) {
            case 'UserInput':
                return this.setState({
                    beforeAdd: {
                        UserInput: true,
                        Question: false,
                        FileUpload: false,
                        Solutions: false
                    }
                });
            case 'Question':
                return this.setState({
                    beforeAdd: {
                        UserInput: false,
                        Question: true,
                        FileUpload: false,
                        Solutions: false
                    }
                });
            case 'FileUpload':
                return this.setState({
                    beforeAdd: {
                        UserInput: false,
                        Question: false,
                        FileUpload: true,
                        Solutions: false
                    }
                });
            case 'Solutions':
                return this.setState({
                    beforeAdd: {
                        UserInput: false,
                        Question: false,
                        FileUpload: false,
                        Solutions: true
                    }
                });
            default:
                return this.setState({
                    beforeAdd: {
                        UserInput: false,
                        Question: false,
                        FileUpload: false,
                        Solutions: false
                    }
                });
        }
    };


    handleNewBlock = (addedBlock) => {
        this.setState(
            {
                beforeAdd: {
                    UserInput: false,
                    Question: false,
                    FileUpload: false,
                    Solutions: false
                }, currentTab: 'UserInput'
            },
            () => this.props.handleAddBlock(addedBlock)
        );

    };

    onChangeTab = (currentTab) => {
        this.setState({currentTab});
    };

    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        return (
            <Modal
                width={800}
                title="Add New Block"
                visible={this.props.visible}
                onOk={this.handleAdd}
                onCancel={this.props.closeModal}
                destroyOnClose={true}
                footer={[
                    <Button key="cancel" onClick={this.props.closeModal}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.onBeforeAdd}>
                        Add
                    </Button>,
                ]}>

                <Tabs type="card" onChange={this.onChangeTab}>
                    <TabPane tab={<span><Icon type="form"/>User Input</span>}
                             key="UserInput">
                        <UserInput layout={formItemLayout}
                                   beforeAdd={this.state.beforeAdd.UserInput}
                                   handleNewBlock={this.handleNewBlock}/>
                    </TabPane>

                    <TabPane tab={<span><Icon type="question-circle"/>Question</span>}
                             key="Question">
                        <Question layout={formItemLayout}
                                  beforeAdd={this.state.beforeAdd.Question}
                                  handleNewBlock={this.handleNewBlock}/>
                    </TabPane>

                    <TabPane tab={<span><Icon type="file-add"/>File Upload</span>}
                             key="FileUpload">
                        <FileUpload layout={formItemLayout}
                                    beforeAdd={this.state.beforeAdd.FileUpload}
                                    handleNewBlock={this.handleNewBlock}/>
                    </TabPane>

                    <TabPane tab={<span><Icon type="tag"/>Solutions</span>}
                             key="Solutions">
                        <Solutions layout={formItemLayout}
                                   beforeAdd={this.state.beforeAdd.Solutions}
                                   handleNewBlock={this.handleNewBlock}/>
                    </TabPane>

                </Tabs>
            </Modal>
        );
    }
}


export default connect()(NewBlockModal)
