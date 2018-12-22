import React from 'react';
import {Form, Button, message, Tabs} from "antd";
import {connect} from 'react-redux';

import "./Profile.less"
import styles from "./Profile.module.less"
import ProfileInput from "./profileComponents/ProfileInput/ProfileInput";

import {profileActions} from "../../../store/actions/profile.actions";

const loading = () => {
    message.loading('Updating...', 0);
};

const TabPane = Tabs.TabPane;

class Profile extends React.Component {
    state = {
        profile: {
            name: "",
            email: "",
            companyName: ""
        },
        newsletters: false,
        profileSettings: {
            statNotifications: false,
            trackData: false,
            techSupport: false,
            accountSpecialist: false
        },
        password: {
            old: "",
            new: "",
            repeat: ""
        },
        formSubmitted: false,
        dataCalled: false,
        dataRendered: false,
        tabIndex: 1
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                if (this.state.isPopupDisabled) {
                    values.secondsUntilPopup = 0
                }
                // send to server
                this.setState({formSubmitted: true});
                switch (this.state.tabIndex) {
                    case 1:
                        this.props.dispatch(profileActions.saveProfileDetails(values));
                        break;
                    case 2:
                        this.props.dispatch(profileActions.saveDataSettings(values));
                        break;
                }
                //loading();
            }
        });
    };

    handleChange = (e) => {
        let name = undefined;
        let value = undefined;
        if (e.target.type === "checkbox") {
            name = e.target.name;
            value = e.target.checked;
        } else {
            name = e.target.name;
            value = e.target.value;
        }
        if (name.includes(".")) {
            const names = name.split(".");
            if (names.length > 2) {
                console.log("More than 2 '.' depth is not supported");
                return null;
            }
            const tempState = {...this.state[names[0]]};

            if (!tempState) {
                return null;
            }

            tempState[names[1]] = value;
            this.setState({[names[0]]: tempState});
        } else {
            this.setState({[name]: value});
        }
        this.props.form.setFieldsValue({
            [name]: value
        });
    };

    updateAllInputsFromState() {
        const tempState = this.state;
        this.props.form.setFieldsValue({
            ["profile.name"]: tempState.profile.name,
            ["profile.email"]: tempState.profile.email,
            ["profile.companyName"]: tempState.profile.companyName,
            ["newsletters"]: tempState.newsletters,
            ["profileSettings.statNotifications"]: tempState.profileSettings.statNotifications,
            ["profileSettings.trackData"]: tempState.profileSettings.trackData,
            ["profileSettings.techSupport"]: tempState.profileSettings.techSupport,
            ["profileSettings.accountSpecialist"]: tempState.profileSettings.accountSpecialist
        });
        this.setState({dataRendered: true});
    }

    updateStateFromProps(nextProps) {
        const data = nextProps.profileData.profile.data;
        if(data && !this.state.dataCalled){
            if(data.user){
                this.setState({
                    profile: {
                        name: data.user.Firstname + " " + data.user.Surname,
                        email: data.user.Email,
                        companyName: data.company.Name
                    }
                });
            }

            if(data.newsletters){
                this.setState({
                    newsletters: data.newsletters
                });
            }

            if(data.userSettings){
                this.setState({
                    profileSettings: {
                        statNotifications: data.userSettings.UserInputNotifications,
                        trackData: data.userSettings.TrackingData,
                        techSupport: data.userSettings.TechnicalSupport,
                        accountSpecialist: data.userSettings.AccountSpecialist
                    }
                });
            }
            this.setState({dataCalled: true});
        }
    }

    componentDidMount() {
        this.props.dispatch(profileActions.getProfile());
    }

    componentWillReceiveProps(nextProps){
        this.updateStateFromProps(nextProps);
    }

    changeTab = (key) => {
        this.setState({tabIndex: parseInt(key)});
    };

    render() {
        if(this.state.dataCalled && !this.state.dataRendered){
            this.updateAllInputsFromState();
        }
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14}
        };
        const {getFieldDecorator} = this.props.form;

        const newsletters = this.state.newsletters;

        const {profileSettings} = this.state;

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
                        <Tabs defaultActiveKey={"1"} onChange={this.changeTab}>
                            <TabPane tab={"Profile Details"} key={"1"}>

                                <Form onSubmit={this.handleSubmit}>
                                    <ProfileInput title={"Name"} name="profile.name"
                                                  rules={{
                                                      required: true,
                                                      message: "Please enter your first and last name here"
                                                  }}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  form={this.props.form}
                                                  description={"Enter your name here"}
                                    />

                                    <ProfileInput title={"Email"} name="profile.email"
                                                  rules={{
                                                      required: true,
                                                      message: "Please enter a valid email"
                                                  }}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange} readOnly={true}
                                                  form={this.props.form}
                                                  description={"Enter your email here (For your security we have temporarily disabled this box until we improve its system"}
                                    />

                                    <ProfileInput title={"Company Name"} name="profile.companyName"
                                                  rules={{
                                                      required: true,
                                                      message: "Please enter your company name"
                                                  }}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  form={this.props.form}
                                                  description={"Enter your company name here"}
                                    />

                                    <br/>

                                    <div style={{textAlign: "center"}}><Button htmlType={"submit"}
                                                                               className={"ant-btn-primary"}>Update</Button>
                                    </div>
                                </Form>

                            </TabPane>
                            <TabPane tab={"Data Settings"} key={"2"}>

                                <Form onSubmit={this.handleSubmit}>
                                    <h2>Data Sharing Settings</h2>
                                    <p>Any data that you collect, process and store on TheSearchBase platform is kept
                                        secure
                                        and confidential at all times. The data that you collect is data that enables
                                        our
                                        software to work at its optimum level.</p>
                                    <h4>This part of the website enables you to control what settings you may share with
                                        us.</h4>

                                    <br/>

                                    <ProfileInput title={"Newsletters"} name="newsletters"
                                                  type={"checkbox"} checked={newsletters}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  description={"We would like to keep you updated with the latest software updates and features available\n" +
                                                  "                                to you, If you decide to not subscribe you may miss on important features and\n" +
                                                  "                                announcements."}>
                                    </ProfileInput>

                                    <br/>

                                    <ProfileInput title={"New Users Counter"} name="profileSettings.statNotifications"
                                                  type={"checkbox"} checked={profileSettings.statNotifications}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  description={"If allowed we will send you the number of new user records your assistants have\n" +
                                                  "                                    stored\n" +
                                                  "                                    every 12 hours through email."}>
                                    </ProfileInput>

                                    <br/>

                                    <strong>Erasing data</strong>
                                    <p>If you decide to stop using our platform, we will simply delete
                                        your information after a year of inactivity.</p>

                                    <br/>

                                    <ProfileInput title={"Tracking Data"} name="profileSettings.trackData"
                                                  type={"checkbox"} checked={profileSettings.trackData}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  description={"We do not in any way track your information for marketing purposes. However we\n" +
                                                  "                                    would recommend allowing us to contact you if we see that\n" +
                                                  "                                        there\n" +
                                                  "                                        are ways we could enhance your bot or use of our software."}>
                                    </ProfileInput>

                                    <br/>

                                    <ProfileInput title={"Technical Support"} name="profileSettings.techSupport"
                                                  type={"checkbox"} checked={profileSettings.techSupport}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  description={"Let our team view your errors and problems in order for us to\n" +
                                                  "                                    solve your issues."}>
                                    </ProfileInput>

                                    <br/>

                                    <ProfileInput title={"Account Specialist"} name="profileSettings.accountSpecialist"
                                                  type={"checkbox"} checked={profileSettings.accountSpecialist}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  description={"Let our team contact you to help make recommendations as to how you can make\n" +
                                                  "                                    your bots more successful and ways to collect more valuable data. If you\n" +
                                                  "                                    don't\n" +
                                                  "                                    have a sales specialist, we recommend you enable this so we can help you make the\n" +
                                                  "                                    most\n" +
                                                  "                                    of our software."}>
                                    </ProfileInput>

                                    <br/>

                                    <div style={{textAlign: "center"}}><Button htmlType={"submit"}
                                                                               className={"ant-btn-primary"}>Update</Button>
                                    </div>
                                </Form>
                            </TabPane>
                            <TabPane tab={"Change Password"} key={"3"}>

                                <Form onSubmit={this.handleSubmit}>
                                    <ProfileInput title={"Old Password"} name="password.old"
                                                  rules={{
                                                      required: true,
                                                      message: "Please enter your old password"
                                                  }}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  form={this.props.form}
                                                  description={"Enter your old password here"}
                                    />

                                    <ProfileInput title={"New Password"} name="password.new"
                                                  rules={{
                                                      required: true,
                                                      message: "Please enter your new password"
                                                  }}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  form={this.props.form}
                                                  description={"Enter your new password here"}
                                    />

                                    <ProfileInput title={"Repeat Password"} name="password.repeat"
                                                  rules={{
                                                      required: true,
                                                      message: "Passwords must match"
                                                  }}
                                                  getFieldDecorator={getFieldDecorator} formItemLayout={formItemLayout}
                                                  handleChange={this.handleChange}
                                                  form={this.props.form}
                                                  description={"Enter your new password again here"}
                                    />

                                    <br/>

                                    <div style={{textAlign: "center"}}><Button htmlType={"submit"}
                                                                               className={"ant-btn-primary"}>Update</Button>
                                    </div>
                                </Form>
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
        profileData: state.profile
    };
}

export default connect(mapStateToProps)(Form.create()(Profile));
