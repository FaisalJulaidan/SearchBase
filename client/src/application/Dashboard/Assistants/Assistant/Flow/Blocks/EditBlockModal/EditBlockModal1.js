import React, {Component} from 'react';

import {http} from "../../../../../../../helpers";

import {Modal} from 'antd';
import UserInput from "./Cards/UserInput";
import Question from "./Cards/Question";
import FileUpload from "./Cards/FileUpload";
import Solutions from "./Cards/Solutions";

class EditBlockModal extends Component {

    state = {
        layout: {
            labelCol: {span: 6},
            wrapperCol: {span: 14}
        },
        blockTypes: [],
        allBlocks: [],
        allGroups: [],
        currentGroup: null
    };

    componentDidMount() {
        http.get(`/assistant/flow/options`)
            .then(res => this.setState({blockTypes: res.data.data.blockTypes}))
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            block: nextProps.block,

            allBlocks: nextProps.blocks,
            allGroups: nextProps.allGroups,
            currentGroup: nextProps.currentGroup
        })
    }

    handleEditBlock = (edittedBlock) => {
        if (edittedBlock)
            this.props.handleEditBlock(edittedBlock);
        this.props.closeModal();
    };

    render() {
        return (
            <Modal width={800}
                   title="Edit Block"
                   visible={this.props.visible}
                   onCancel={this.props.closeModal}
                   destroyOnClose={true}
                   footer={null}>

                {this.props.block.type === "User Input" ?
                    <UserInput options={this.state} handleEditBlock={this.handleEditBlock}/> : null}
                {this.props.block.type === "Question" ?
                    <Question options={this.state} handleEditBlock={this.handleEditBlock}/> : null}
                {this.props.block.type === "File Upload" ?
                    <FileUpload options={this.state} handleEditBlock={this.handleEditBlock}/> : null}
                {this.props.block.type === "Solutions" ?
                    <Solutions options={this.state} handleEditBlock={this.handleEditBlock}/> : null}
            </Modal>
        );
    }
}


export default EditBlockModal
