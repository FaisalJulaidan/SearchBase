import React, {Component} from 'react';

import {http} from "../../../../../../../helpers";

import {Modal} from 'antd';
import UserInput from "../CardTypes/UserInput";
import Question from "../CardTypes/Question";
import FileUpload from "../CardTypes/FileUpload";
import Solutions from "../CardTypes/Solutions";

class EditBlockModal extends Component {

    state = {
        layout: {
            labelCol: {span: 6},
            wrapperCol: {span: 14}
        },
        flowOptions: [],
        allBlocks: [],
        allGroups: [],
        currentGroup: null
    };

    componentDidMount() {
        http.get(`/assistant/flow/options`)
            .then(res => this.setState({flowOptions: res.data.data}))
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            block: nextProps.block,

            allBlocks: nextProps.allBlocks,
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

                {this.props.block.Type === "User Input" ?
                    <UserInput options={this.state} handleEditBlock={this.handleEditBlock}
                               handleDeleteBlock={this.props.handleDeleteBlock}/> : null}
                {this.props.block.Type === "Question" ?
                    <Question options={this.state} handleEditBlock={this.handleEditBlock}
                              handleDeleteBlock={this.props.handleDeleteBlock}/> : null}
                {this.props.block.Type === "File Upload" ?
                    <FileUpload options={this.state} handleEditBlock={this.handleEditBlock}
                                handleDeleteBlock={this.props.handleDeleteBlock}/> : null}
                {this.props.block.Type === "Solutions" ?
                    <Solutions options={this.state} handleEditBlock={this.handleEditBlock}
                               handleDeleteBlock={this.props.handleDeleteBlock}/> : null}
            </Modal>
        );
    }
}


export default EditBlockModal
