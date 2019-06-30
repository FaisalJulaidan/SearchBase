import React, {Component} from 'react';
import styles from "./Groups.module.less";
import {Button, List, Skeleton, Row, Modal, Menu, Empty, Col} from "antd";
import NewGroup from "./NewGroup/NewGroup";
import EditGroup from "./EditGroup/EditGroup";

const confirm = Modal.confirm;

const content = (
    <div>
        <p>Content</p>
        <p>Content</p>
    </div>
);

class Groups extends Component {

    state = {
        newGroupModal: false,
        editGroupModal: false,
        selectedGroupToEdit: {}
    };

    componentWillReceiveProps(nextProps) {
        // This handles when updating the selected group to show its blocks
        if (nextProps.currentGroup !== this.state.currentGroup && nextProps.currentGroup) {
            this.setState({selectedGroupToEdit: nextProps.currentGroup.blocks})
        }
    }

    ////// ADD GROUP
    handleAddGroup = (newGroup) => {
        this.props.addGroup(newGroup);
        this.setState({newGroupModal: false});
    };

    handleAddGroupCancel = () => this.setState({newGroupModal: false});

    showNewGroupModal = () => this.setState({newGroupModal: true});


    ////// EDIT GROUP
    handleEditGroup = (editedGroup) => {
        this.props.editGroup(editedGroup);
        this.setState({editGroupModal: false});
    };

    handleEditGroupCancel = () => this.setState({editGroupModal: false});

    showEditGroupModal = () => this.setState({editGroupModal: true});

    ////// DELETE GROUP
    handleDeleteGroup = (deletedGroup) => {
        confirm({
            title: `Delete group confirmation`,
            content: `If you click OK, this group will be deleted with its associated blocks forever`,
            okType: 'danger',
            onOk: () => {
                this.props.deleteGroup(deletedGroup);
                this.setState({editGroupModal: false, selectedGroupToEdit: {}});
            }
        });
    };


    render() {
        const {groupsList} = this.props;
        return (
            <>
                <Row>

                    {
                        groupsList ?
                            <Col xs={{ span: 14}} lg={{ span: 17}}>

                                <Menu mode="horizontal" selectedKeys={[this.props.currentGroup.name]}>
                                    {
                                        this.props.groupsList.map((group, index) =>
                                            <Menu.Item onClick={() => this.props.selectGroup(group)} key={group.name}>
                                                {group.name}
                                            </Menu.Item>

                                        )
                                    }
                                </Menu>

                            </Col>
                            :
                            null
                    }

                    <Col xs={{ span: 10}} lg={{ span: 7}} style={{paddingTop: 20, textAlign: groupsList ? "right" : "left"}}>
                        <Button
                            style={{marginRight: 10}}
                            onClick={this.showNewGroupModal}
                            type="default"
                            size={"small"}
                            icon="plus"
                        >
                            Add group
                        </Button>
                        <Button
                            type="default"
                            size={"small"}
                            icon="edit"
                            disabled={!(!!this.props.currentGroup.name)}
                            onClick={() => this.showEditGroupModal()}>
                            Edit
                        </Button>
                    </Col>
                </Row>


                <NewGroup visible={this.state.newGroupModal}
                          handleCancel={this.handleAddGroupCancel}
                          handleSave={this.handleAddGroup}/>




                <EditGroup group={this.props.currentGroup}
                           visible={this.state.editGroupModal}
                           handleCancel={this.handleEditGroupCancel}
                           handleUpdate={this.handleEditGroup}
                           handleDelete={this.handleDeleteGroup}/>
            </>
        );
    }
}

export default Groups;
