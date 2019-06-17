import React from "react";
import {store} from "store/store";
import {usersManagementActions} from "store/actions";
import {Button, Table, Divider, Tag, Modal} from 'antd';
import {isEmpty} from "lodash";
import AddUserModal from "./Modals/AddUserModal";
import EditUserModal from "./Modals/EditUserModal";
import styles from "./UsersDisplay.less"
import {getUser} from "helpers";

const confirm = Modal.confirm;

class UsersDisplay extends React.Component {

    state = {
        addUserModalVisible: false,
        editUserModalVisible: false,
        userToEdit: null
    };

    constructor(props) {
        super(props);
        this.columns = [
            {
                title: 'Role',
                key: 'Role',
                width: '5%',
                render: (text, record) => (
                    <Tag color={record.role.Name === 'Owner' ? 'purple' : null }>
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
                render: (text, record) => (
                    <>
                        {record.role.Name === 'Owner' ? null :
                            <span>
                                <a onClick={() => this.showEditUserModal(record)}>
                                    Edit
                                </a>
                                <Divider type="vertical" />
                                <a onClick={() => {this.deleteUser(record?.user.ID)}}>
                                    Delete
                                </a>
                            </span>
                        }
                    </>
                ),
            },
        ];
    }

    addUser = (user) => {
        store.dispatch(usersManagementActions.addUser({user:user}));
    };

    editUser = (userID, values) => {
        store.dispatch(usersManagementActions.editUser(userID, values));
    };

    deleteUser = (userID) => {
        confirm({
            title: `Delete user confirmation`,
            content: `If you click OK, this user will be deleted and its associated details forever`,
            onOk: () => {
                this.props.dispatch(usersManagementActions.deleteUser(userID));
            }
        });
    };

    showAddUserModal = () => this.setState({addUserModalVisible: true});

    hideAddUserModal = () => this.setState({addUserModalVisible: false});

    showEditUserModal = (user) => this.setState({editUserModalVisible: true, userToEdit: user});

    hideEditUserModal = () => this.setState({editUserModalVisible: false});


    render() {
        const {users, roles} = this.props;
        return (
            <>
                <div style={{textAlign: "right"}}>
                    <Button style={{marginBottom: "10px"}} type="primary"
                            icon="plus"
                            onClick={this.showAddUserModal}>
                        Add User
                    </Button>
                </div>

                <Table
                    bordered
                    dataSource={users}
                    columns={this.columns}
                    scroll={{ x: 600 }}
                />

                <AddUserModal
                    roles={roles}
                    visible={this.state.addUserModalVisible}
                    handleCancel={this.hideAddUserModal}
                    handleSave={this.addUser}
                />

                <EditUserModal
                    userData={this.state.userToEdit}
                    roles={roles}
                    visible={this.state.editUserModalVisible}
                    handleCancel={this.hideEditUserModal}
                    handleSave={this.editUser}
                />
            </>
        );
    }
}

export default UsersDisplay;