import React from "react";
import styles from "./UsersManagement.module.less";
import {Tabs} from "antd";
import connect from "react-redux/es/connect/connect";
import {usersManagementActions} from "../../../../store/actions";

const TabPane = Tabs.TabPane;

class UsersManagement extends React.Component {

    componentDidMount() {
        this.props.dispatch(usersManagementActions.getUsers())
    }

    render () {
        console.log(this.state)
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

                            </TabPane>

                            <TabPane tab={"Roles' Permissions"} key={"2"}>

                            </TabPane>
                        </Tabs>
                    </div>
                </div>
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        usersData: state.usersList
    };
}

export default connect(mapStateToProps)(UsersManagement)