import React, {Component} from 'react';

import {http} from "../../../../../../../helpers";

import {Icon, Modal, Tabs} from 'antd';

import UserInput from "../CardTypes/UserInput";
import Question from "../CardTypes/Question";
import FileUpload from "../CardTypes/FileUpload";
import Solutions from "../CardTypes/Solutions";
import NewDataCategoryModal from "../../../../../../../components/Modals/NewDataCategoryModal/NewDataCategoryModal";

const TabPane = Tabs.TabPane;

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

    // componentDidMount() {
    //     http.get(`/assistant/flow/options`)
    //         .then(res => this.setState({flowOptions: res.data.data}))
    // }

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
        this.props.closeModal();
    };

    onChangeTab = (currentTab) => this.setState({currentTab});

    render() {
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
                            <UserInput modalState={this.state}
                                       addNewDataCategory={this.showNewDataCategoryModal}
                                       handleNewBlock={this.handleNewBlock}
                                       options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="question-circle"/>Question</span>}
                                 key="Question">
                            <Question modalState={this.state}
                                      handleNewBlock={this.handleNewBlock}
                                      options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="file-add"/>File Upload</span>}
                                 key="FileUpload">
                            <FileUpload modalState={this.state}
                                        handleNewBlock={this.handleNewBlock}
                                        options={this.props.options}/>
                        </TabPane>

                        <TabPane tab={<span><Icon type="tag"/>Solutions</span>}
                                 key="Solutions">
                            <Solutions modalState={this.state}
                                       handleNewBlock={this.handleNewBlock}
                                       options={this.props.options}/>
                        </TabPane>

                    </Tabs>
                </Modal>


            </div>



        );
    }
}


export default NewBlockModal
