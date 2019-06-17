import React from "react";
import {Tabs, Modal, Typography, Spin} from "antd";
import connect from "react-redux/es/connect/connect";

import './UsersManagement.less';
import styles from "./UsersManagement.module.less"

import {usersManagementActions} from "store/actions";
import UsersDisplay from "./UsersDisplay/UsersDisplay";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'

const {Title, Paragraph} = Typography;
const TabPane = Tabs.TabPane;
const confirm = Modal.confirm;


class UsersManagement extends React.Component {

    componentDidMount() {
        this.props.dispatch(usersManagementActions.getUsers());
    }


    render () {
        const {usersList, roles} = this.props;
        return (
                <>
                    {this.props.isLoading ? <Spin/> :
                        <NoHeaderPanel>
                            <div className={styles.Header}>
                                <Title className={styles.Title}>
                                    Users Management
                                </Title>
                                <Paragraph type="secondary">
                                    Here you can edit other users under your company and what permissions they have.
                                </Paragraph>
                            </div>

                            <div className={[styles.Body, 'usersTabs'].join(' ')}>
                                {!usersList ? <Spin/> :

                                    <Tabs defaultActiveKey={'1'} size={"large"} animated={false}>
                                        <TabPane tab={"Users"} key={"1"}>
                                            <UsersDisplay
                                                users={usersList}
                                                roles={roles}
                                                addUser={this.addUser}
                                                editUser={this.editUser}
                                                deleteUser={this.deleteUser}
                                            />
                                        </TabPane>

                                        <TabPane disabled={true} tab={"Permissions (coming soon)"} key={"2"}>
                                            Coming soon...
                                        </TabPane>
                                    </Tabs>
                                }
                            </div>
                        </NoHeaderPanel>
                    }
                </>
        )
    }
}

function mapStateToProps(state) {
    return {
        usersList: state.usersManagement.usersList,
        roles: state.usersManagement.roles,
        isLoading: state.usersManagement.isLoading
    };
}

export default connect(mapStateToProps)(UsersManagement)