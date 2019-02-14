import React, {Component} from 'react';
import styles from "./Groups.module.less";
import {Avatar, Button, List, Skeleton, Spin, Modal} from "antd";
import NewGroup from "./NewGroup/NewGroup";
import EditGroup from "./EditGroup/EditGroup";

const confirm = Modal.confirm;

class Groups extends Component {

    state = {
        newGroupModal: false,
        editGroupModal: false,
        selectedGroupToEdit: {}
    };


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
        this.setState({editGroupModal: false, selectedGroupToEdit: {}});
    };

    handleEditGroupCancel = () => this.setState({editGroupModal: false});

    showEditGroupModal = (item) => this.setState({editGroupModal: true, selectedGroupToEdit: item});

    ////// DELETE GROUP
    handleDeleteGroup = (deletedGroup) => {
        confirm({
            title: `Delete group confirmation`,
            content: `If you click OK, this group will be deleted with its associated blocks forever`,
            onOk: () => {
                this.props.deleteGroup(deletedGroup);
                this.setState({editGroupModal: false, selectedGroupToEdit: {}});
            }
        });
    };


    render() {
        return (
            <div className={styles.Panel}>
                <div className={styles.Panel_Header}>
                    <div>
                        <h3>Flow Groups</h3>
                    </div>
                    <div>
                        <Button className={styles.Panel_Header_Button} type="primary" icon="plus"
                                onClick={this.showNewGroupModal}>
                            Add Group
                        </Button>

                        <NewGroup visible={this.state.newGroupModal}
                                  handleCancel={this.handleAddGroupCancel}
                                  handleSave={this.handleAddGroup}/>
                    </div>
                </div>


                <div className={styles.Panel_Body}>
                    {
                        this.props.isLoading ?
                            <Spin><Skeleton active={true}/></Spin>
                            :
                            <List
                                itemLayout="horizontal"
                                dataSource={this.props.groupsList}
                                renderItem={item => (
                                    <List.Item actions={[<Button icon={'edit'}
                                                                 onClick={() => this.showEditGroupModal(item)}/>]}>
                                        <List.Item.Meta
                                            onClick={() => this.props.selectGroup(item)}
                                            className={styles.groupsList}
                                            avatar={<Avatar icon="ordered-list" style={{backgroundColor: '#9254de'}}/>}
                                            title={item.name}
                                            description={item.description}
                                        />
                                    </List.Item>
                                )}
                            />
                    }
                </div>

                <EditGroup group={this.state.selectedGroupToEdit}
                           visible={this.state.editGroupModal}
                           handleCancel={this.handleEditGroupCancel}
                           handleUpdate={this.handleEditGroup}
                           handleDelete={this.handleDeleteGroup}/>
            </div>
        );
    }
}

export default Groups;
