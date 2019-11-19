import React from "react";
import {store} from "store/store";
import {usersManagementActions} from "store/actions";
import {Button, Table, Divider, Tag, Modal} from 'antd';
import {isEmpty} from "lodash";
import "./Roles.less"
import {getUser, getRole} from "helpers";

const confirm = Modal.confirm;

class Roles extends React.Component {

    state = {
        addRoleModalVisible: false,
        editRoleModalVisible: false,
        roleToEdit: null
    };

    constructor(props) {
        super(props);
        this.columns = [
            {
                title: 'Role Name',
                key: 'Name',
                render: (text, record) => (
                    <Tag>
                        {record.Name}
                    </Tag>),

            },
            {
                title: 'Add Users',
                key: 'AddUsers',
                render: (text, record) => (<p align="center">{record.AddUsers ? 'Yes' : 'No'}</p>),

            },
            {
                title: 'Edit Users',
                key: 'EditUsers',
                render: (text, record) => (<p align="center">{record.EditUsers ? 'Yes' : 'No'}</p>),
            },
            {
                title: 'Delete Users',
                key: 'DeleteUsers',
                render: (text, record) => (<p align="center">{record.DeleteUsers ? 'Yes' : 'No'}</p>),
            },
            {
                title: 'Edit Assistant Script',
                key: 'EditChatbots',
                render: (text, record) => (<p align="center">{record.EditChatbots ? 'Yes' : 'No'}</p>),
            },
            {
                title: 'Access Billing',
                key: 'AccessBilling',
                render: (text, record) => (<p align="center">{record.AccessBilling ? 'Yes' : 'No'}</p>),
            },
        ];
    }

    addRole = (role) => {
       return;
    };

    editRole = (roleID, values) => {
        return;
    };

    deleteRole = (roleID) => {
        // TODO deleting roles what does it mean for other users who has that role?
        confirm({
            title: `Delete role confirmation`,
            content: `If you click OK, this role....`,
            onOk: () => {
                // store.dispatch(usersManagementActions.deleteUser(userID));
            }
        });
    };

    showAddRoleModal = () => this.setState({addRoleModalVisible: true});

    hideAddRoleModal = () => this.setState({addRoleModalVisible: false});

    showEditRoleModal = (user) => this.setState({editRoleModalVisible: true, roleToEdit: user});

    hideEditRoleModal = () => this.setState({editRoleModalVisible: false});


    render() {
        const {roles, isLoading} = this.props;
        return (
            <>
                    <div style={{textAlign: "right"}}>
                        <Button style={{marginBottom: "10px"}} type="primary"
                                icon="plus"
                                onClick={this.showAddRoleModal}
                                disabled={true}>
                            Add Role (coming soon)
                        </Button>
                    </div>

                    < Table
                    bordered
                    dataSource={roles}
                    columns={this.columns}
                    scroll={{ x: 'max-content' }}
                    loading={isLoading}
                    />
            </>
        );
    }
}

export default Roles;