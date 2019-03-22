import React, {Component} from 'react';
import styles from "./Groups.module.less";
import {Button, List, Skeleton, Spin, Modal, Menu, Empty} from "antd";
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
            <div className={styles.Panel}>
                <div className={styles.Panel_Header_With_Button}>
                    <div>
                        <h3>Groups</h3>
                    </div>
                    <div>
                        <Button className={styles.Panel_Header_Button}
                                type="default"
                                size={"small"}
                                icon="plus"
                                onClick={this.showNewGroupModal}>
                            Add
                        </Button>

                        <Button className={styles.Panel_Header_Button}
                                type="default"
                                size={"small"}
                                icon="plus"
                                disabled={!(!!this.props.currentGroup.name)}
                                onClick={() => this.showEditGroupModal()}>
                            Edit
                        </Button>

                        <NewGroup visible={this.state.newGroupModal}
                                  handleCancel={this.handleAddGroupCancel}
                                  handleSave={this.handleAddGroup}/>
                    </div>
                </div>


                <div className={styles.Panel_Body}>

                    <Menu mode="inline" defaultSelectedKeys={['0']}>
                        {
                            groupsList ?
                            this.props.groupsList.map((group, index) =>
                                <Menu.Item onClick={() => this.props.selectGroup(group)} key={index}>
                                    {group.name}
                                </Menu.Item>
                            ) : <Empty description={'No groups yet'}>
                                    <Button type="primary" onClick={this.showNewGroupModal}>Create Now</Button>
                                </Empty>
                        }
                    </Menu>

                </div>

                <EditGroup group={this.props.currentGroup}
                           visible={this.state.editGroupModal}
                           handleCancel={this.handleEditGroupCancel}
                           handleUpdate={this.handleEditGroup}
                           handleDelete={this.handleDeleteGroup}/>
            </div>
        );
    }
}

export default Groups;
