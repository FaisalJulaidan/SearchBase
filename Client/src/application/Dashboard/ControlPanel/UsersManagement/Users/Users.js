import React from "react";
import {store} from "store/store";
import {usersManagementActions} from "store/actions";
import {Button, Table, Divider, Tag, Modal} from 'antd';
import {isEmpty} from "lodash";
import "./Users.less"
import AddUserModal from "./Modals/AddUserModal";
import EditUserModal from "./Modals/EditUserModal";
import {getUser, getRole} from "helpers";

const confirm = Modal.confirm;

class Users extends React.Component {

    state = {
        addUserModalVisible: false,
        editUserModalVisible: false,
        userToEdit: null
    };

    constructor(props) {
        super(props);
        this.currentUserRole = getRole();
        this.currentUser = getUser();
        this.columns = [
            {
                title: 'Role',
                key: 'Role',
                width: '5%',
                render: (text, record) => (
                    <Tag>
                        {record.role.Name}
                    </Tag>),

            },
            {
                title: 'First name',
                key: 'Firstname',
                render: (text, record) => (<p>{record.user.Firstname}</p>),

            },
            {
                title: 'Surname',
                key: 'Surname',
                render: (text, record) => (<p>{record.user.Surname}</p>),
            },
            {
                title: 'Email',
                key: 'Email',
                render: (text, record) => (<p>{record.user.Email}</p>),
            },
            {
                title: 'Phone Number',
                key: 'PhoneNumber',
                render: (text, record) => (<p>{record.user.PhoneNumber}</p>),
            },
            {
                title: 'Last Access',
                key: 'LastAccess',
                render: (text, record) => (<p>{record.user.LastAccess || 'Never'}</p>),
            },
            {
                title: 'Verified',
                key: 'Verified',
                render: (text, record) => (
                    <>
                        { record.user.Verified ?
                            <Tag color="#87d068">
                                Verified
                            </Tag>
                            :
                            <Tag color={'red'}>
                                Unverified
                            </Tag>
                        }
                    </>
                    ),

            },
            {
                title: 'Action',
                key: 'action',
                render: (text, record) => {
                    const isYou = this.currentUser.email === record.user.Email;
                    return (
                        <>
                            {(record.role.Name === 'Owner' && !(this.currentUserRole.Name === 'Owner')) ? null :

                                isYou ? <Tag color={'purple'}>You</Tag> :
                                    <span>
                                <Button type="link"
                                        onClick={() => this.showEditUserModal(record)}
                                        disabled={!this.currentUserRole.EditUsers ||
                                        this.currentUser.email === record.user.Email}>
                                    Edit
                                </Button>
                                <Divider type="vertical" />
                                <Button type="link"
                                        onClick={() => {this.deleteUser(record.user.ID)}}
                                        disabled={!this.currentUserRole.DeleteUsers ||
                                        this.currentUser.email === record.user.Email}>
                                    Delete
                                </Button>
                            </span>
                            }
                        </>
                    )
                }

            },
        ];
    }

    addUser = (user) => {
        store.dispatch(usersManagementActions.addUser(user));
        this.hideAddUserModal()
    };

    editUser = (userID, values) => {
        store.dispatch(usersManagementActions.editUser(userID, values));
        this.hideEditUserModal()
    };

    deleteUser = (userID) => {
        confirm({
            title: `Delete user confirmation`,
            content: `If you click OK, this user will be deleted and its associated details forever`,
            onOk: () => {
                store.dispatch(usersManagementActions.deleteUser(userID));
            }
        });
    };

    showAddUserModal = () => this.setState({addUserModalVisible: true});

    hideAddUserModal = () => this.setState({addUserModalVisible: false});

    showEditUserModal = (user) => this.setState({editUserModalVisible: true, userToEdit: user});

    hideEditUserModal = () => this.setState({editUserModalVisible: false});


    render() {
        const {users, roles, isLoading} = this.props;
        return (
            <>
                <div style={{textAlign: "right"}}>
                    <Button style={{marginBottom: "10px"}} type="primary"
                            icon="plus"
                            onClick={this.showAddUserModal}
                            disabled={!this.currentUserRole.AddUsers}>
                        Add User
                    </Button>
                </div>

                < Table
                bordered
                dataSource={users}
                columns={this.columns}
                scroll={{ x: 'max-content' }}
                loading={isLoading}

                />

                <AddUserModal
                roles={roles}
                visible={this.state.addUserModalVisible}
                hideModal={this.hideAddUserModal}
                handleSave={this.addUser}
                />

                <EditUserModal
                userData={this.state.userToEdit}
                roles={roles}
                visible={this.state.editUserModalVisible}
                hideModal={this.hideEditUserModal}
                handleSave={this.editUser}
                />
            </>
        );
    }
}

export default Users;