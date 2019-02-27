import React from 'react';
import {Form, Button, message, Tabs} from "antd";
import {connect} from 'react-redux';
import {isEmpty} from "lodash";

import styles from "./Profile.module.less"
import ProfileDetails from "./profileComponents/ProfileDetails/ProfileDetails";
import DataSettings from "./profileComponents/DataSettings/DataSettings";
import ChangePassword from "./profileComponents/ChangePassword/ChangePassword";

import {profileActions} from "../../../../store/actions/profile.actions";
const TabPane = Tabs.TabPane;

class Profile extends React.Component {
    // state = {
    //     password: {
    //         old: "",
    //         new: "",
    //         repeat: ""
    //     }
    // };

    saveProfileDetails = (values) => {
        this.props.dispatch(profileActions.saveProfileDetails(values));
    };

    saveDataSettings = (values) => {
        this.props.dispatch(profileActions.saveDataSettings(values));
    };

    savePassword = (values) => {
        this.props.dispatch(profileActions.changePassword(values.oldPassword, values.newPassword));
    };



    componentDidMount() {
        this.props.dispatch(profileActions.getProfile());
    }

    render() {

        return (
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>User Profile</h3>
                            <p>Here you can edit your details and how we handle your data.</p>
                        </div>
                    </div>

                    <div className={styles.Panel_Body} style={{overflowY: "auto"}}>
                        <Tabs defaultActiveKey={"1"}>
                            <TabPane tab={"Conversation Details"} key={"1"}>
                                <ProfileDetails profileData={this.props.profileData} saveProfileDetails={this.saveProfileDetails}/>
                            </TabPane>

                            <TabPane tab={"Data Settings"} key={"2"}>
                                <DataSettings profileData={this.props.profileData} saveDataSettings={this.saveDataSettings}/>
                            </TabPane>

                            <TabPane tab={"Change Password"} key={"3"}>
                                <ChangePassword savePassword={this.savePassword}/>
                            </TabPane>
                        </Tabs>
                    </div>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        profileData: state.profile.profile
    };
}

export default connect(mapStateToProps)(Form.create()(Profile));
