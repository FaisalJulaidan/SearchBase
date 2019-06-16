import React from "react";
import styles from "./UsersManagement.module.less";
import {Tabs, Modal} from "antd";
import connect from "react-redux/es/connect/connect";
import {usersManagementActions} from "../../../../store/actions";
import UsersDisplay from "./UsersDisplay/UsersDisplay";

const TabPane = Tabs.TabPane;
const confirm = Modal.confirm;


class UsersManagement extends React.Component {

    componentDidMount() {
        this.props.dispatch(usersManagementActions.getUsers());
    }

    addUser = (user) => {
        this.props.dispatch(usersManagementActions.addUser({user:user}));
    };

    editUser = (user) => {
        this.props.dispatch(usersManagementActions.editUser({user:user}));
    };

    deleteUser = (user) => {
        confirm({
            title: `Delete user confirmation`,
            content: `If you click OK, this user will be deleted and its associated details forever`,
            onOk: () => {
                this.props.dispatch(usersManagementActions.deleteUser({user:user}));
            }
        });
    };

    render () {
        return (
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>Users Management</h3>
                            <p>Here you can edit other users under your company and what permissions they have.</p>
                        </div>
                    </div>

                    <div className={styles.Panel_Body} style={{overflowY: "auto"}}>
                        <Tabs defaultActiveKey={"1"}>
                            <TabPane tab={"Users"} key={"1"}>
                                <UsersDisplay
                                    users={this.props.usersData.users}
                                    addUser={this.addUser}
                                    editUser={this.editUser}
                                    deleteUser={this.deleteUser}
                                />
                            </TabPane>

                            {/*<TabPane tab={"Permissions"} key={"2"}>*/}
                                {/*Coming soon...*/}
                            {/*</TabPane>*/}
                        </Tabs>
                    </div>
                </div>
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        usersData: state.usersManagement.usersList
    };
}

export default connect(mapStateToProps)(UsersManagement)