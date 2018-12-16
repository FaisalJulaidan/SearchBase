import React, {Component} from 'react';

import {http} from "../../../../../../../helpers";

import {Button, Modal, Icon, Tabs} from 'antd';

import UserInput from "./Cards/UserInput";
import Question from "./Cards/Question";
import FileUpload from "./Cards/FileUpload";
import Solutions from "./Cards/Solutions";

const TabPane = Tabs.TabPane;

class NewBlockModal extends Component {

    /*
    *       EXPLANATION FOR THE LOGIC IN THIS COMPONENT
    *
    *       The logic here is to have all the data editing inside the cards
    *       in order to collect the data from tabs, there is beforeAdd object
    *       it has all tabs types and we run the one who is active
    *       scenario after you open the modal:
    *
    *       1- select any tab (default = UserInput).
    *
    *       2- when select add it triggers the beforeAdd by change the state in ƒ(onBeforeAdd).
    *
    *       3- after change the state of beforeAdd for the active tab
    *          ƒ(componentWillReceiveProps) will be running inside the active tab only.
    *
    *       4- ƒ(componentWillReceiveProps) will validate the form then run ƒ(handleNewBlock).
    *
    *       5- ƒ(handleNewBlock) will receive the new added block, and pass it to his parent (Blocks.js)
    *          to be send to the server in (Flow.js) and reset the state to the default value.
    */

    state = {
        beforeAdd: {UserInput: false, Question: false, FileUpload: false, Solutions: false},
        currentTab: 'UserInput',
        layout: {
            labelCol: {span: 6},
            wrapperCol: {span: 14}
        },
        blockTypes: []
    };

    componentDidMount() {
        http.get(`/assistant/flow/options`)
            .then(res => this.setState({blockTypes: res.data.data.blockTypes}))
    }


    onBeforeAdd = () => {
        // To send the data of the active tab only
        switch (this.state.currentTab) {
            case 'UserInput':
                return this.setState({
                    beforeAdd: {UserInput: true, Question: false, FileUpload: false, Solutions: false}
                });
            case 'Question':
                return this.setState({
                    beforeAdd: {UserInput: false, Question: true, FileUpload: false, Solutions: false}
                });
            case 'FileUpload':
                return this.setState({
                    beforeAdd: {UserInput: false, Question: false, FileUpload: true, Solutions: false}
                });
            case 'Solutions':
                return this.setState({
                    beforeAdd: {UserInput: false, Question: false, FileUpload: false, Solutions: true}
                });
            default:
                return this.setState({
                    beforeAdd: {UserInput: false, Question: false, FileUpload: false, Solutions: false}
                });
        }
    };

    handleNewBlock = (addedBlock) => {
        if (addedBlock)
        // Reset state & add the new block
            this.setState({
                beforeAdd: {UserInput: false, Question: false, FileUpload: false, Solutions: false},
                currentTab: 'UserInput'
            }, () => {
                this.props.closeModal();
                this.props.handleAddBlock(addedBlock)
            });
        else
        // reset the event beforeAdd
            this.setState({
                beforeAdd: {UserInput: false, Question: false, FileUpload: false, Solutions: false}
            })
    };

    onChangeTab = (currentTab) => this.setState({currentTab});

    render() {
        return (
            <Modal width={800}
                   title="Add New Block"
                   visible={this.props.visible}
                   onOk={this.handleAdd}
                   onCancel={this.props.closeModal}
                   destroyOnClose={true}
                   footer={[
                       <Button key="cancel" onClick={this.props.closeModal}>Cancel</Button>,
                       <Button key="submit" type="primary" onClick={this.onBeforeAdd}>
                           Add
                       </Button>
                   ]}>

                <Tabs type="card" onChange={this.onChangeTab}>
                    <TabPane tab={<span><Icon type="form"/>User Input</span>}
                             key="UserInput">
                        <UserInput options={this.state}
                                   beforeAdd={this.state.beforeAdd.UserInput}
                                   handleNewBlock={this.handleNewBlock}/>
                    </TabPane>

                    <TabPane tab={<span><Icon type="question-circle"/>Question</span>}
                             key="Question">
                        <Question options={this.state}
                                  beforeAdd={this.state.beforeAdd.Question}
                                  handleNewBlock={this.handleNewBlock}/>
                    </TabPane>

                    <TabPane tab={<span><Icon type="file-add"/>File Upload</span>}
                             key="FileUpload">
                        <FileUpload options={this.state}
                                    beforeAdd={this.state.beforeAdd.FileUpload}
                                    handleNewBlock={this.handleNewBlock}/>
                    </TabPane>

                    <TabPane tab={<span><Icon type="tag"/>Solutions</span>}
                             key="Solutions">
                        <Solutions options={this.state}
                                   beforeAdd={this.state.beforeAdd.Solutions}
                                   handleNewBlock={this.handleNewBlock}/>
                    </TabPane>

                </Tabs>
            </Modal>
        );
    }
}


export default NewBlockModal
