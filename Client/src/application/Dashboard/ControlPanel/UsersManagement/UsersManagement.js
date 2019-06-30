import React from "react";
import {Tabs, Typography} from "antd";
import connect from "react-redux/es/connect/connect";

import './UsersManagement.less';
import styles from "./UsersManagement.module.less"

import {usersManagementActions} from "store/actions";
import Users from "./Users/Users";
import Roles from "./Roles/Roles";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'

const {Title, Paragraph} = Typography;
const TabPane = Tabs.TabPane;


class UsersManagement extends React.Component {

    componentDidMount() {
        this.props.dispatch(usersManagementActions.getUsers());
    }


    render () {
        const {usersList, roles, isLoading} = this.props;
        return (
                <>
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
                                    <Tabs defaultActiveKey={'1'} size={"large"} animated={false}>
                                        <TabPane tab={"Users"} key={"1"}>
                                            <Users
                                                users={usersList}
                                                roles={roles}
                                                isLoading={isLoading}
                                            />
                                        </TabPane>

                                        <TabPane tab={"Roles"} key={"2"}>
                                            <Roles
                                                roles={roles}
                                                isLoading={isLoading}
                                            />
                                        </TabPane>
                                    </Tabs>
                            </div>
                        </NoHeaderPanel>
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