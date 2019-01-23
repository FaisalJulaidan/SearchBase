import React, {Component} from 'react';

import {http} from "../../../../../../../helpers";

import {Icon, Modal, Tabs} from 'antd';

import UserInput from "./Cards/UserInput";
import Question from "./Cards/Question";
import FileUpload from "./Cards/FileUpload";
import Solutions from "./Cards/Solutions";
import NewDataCategoryModal from "../../../../../../../components/Modals/NewDataCategoryModal/NewDataCategoryModal";

const TabPane = Tabs.TabPane;

class NewBlockModal extends Component {

    state = {
        layout: {
            labelCol: {span: 6},
            wrapperCol: {span: 14}
        },
        flowOptions: {},
        blocks: [],
        allGroups: [],
        currentGroup: null,
    };

    componentDidMount() {
        http.get(`/assistant/flow/options`)
            .then(res => this.setState({flowOptions: res.data.data}))
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            blocks: nextProps.blocks,
            allGroups: nextProps.allGroups,
            currentGroup: nextProps.currentGroup,
        })
    }

    handleNewBlock = (newBlock) => {
        if (newBlock)
            this.props.handleAddBlock(newBlock);
        this.props.closeModal();
    };

    onChangeTab = (currentTab) => this.setState({currentTab});

    render() {
        console.log(this.state.flowOptions);
        return (
            <div>
                <Modal width={800}
                       title="Add New Block"
                       visible={this.props.visible}
                       onCancel={this.props.closeModal}
                       destroyOnClose={true}
                       footer={null}>

                    <Tabs type="card" onChange={this.onChangeTab}>
                        <TabPane tab={<span><Icon type="form"/>User Input</span>}
                                 key="UserInput">
                            <UserInput options={this.state}
                                       addNewDataCategory={this.showNewDataCategoryModal}
                                       handleNewBlock={this.handleNewBlock}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="question-circle"/>Question</span>}
                                 key="Question">
                            <Question options={this.state}
                                      handleNewBlock={this.handleNewBlock}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="file-add"/>File Upload</span>}
                                 key="FileUpload">
                            <FileUpload options={this.state}
                                        handleNewBlock={this.handleNewBlock}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="tag"/>Solutions</span>}
                                 key="Solutions">
                            <Solutions options={this.state}
                                       handleNewBlock={this.handleNewBlock}/>
                        </TabPane>

                    </Tabs>
                </Modal>


            </div>



        );
    }
}


export default NewBlockModal
