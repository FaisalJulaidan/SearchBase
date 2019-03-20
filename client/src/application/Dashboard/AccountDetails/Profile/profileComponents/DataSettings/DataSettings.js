import React from "react";
import {Button, Form, Switch} from "antd";
import {isEmpty} from "lodash";

const FormItem = Form.Item;

class DataSettings extends React.Component {
    state = {
        newsletters: false,
        statNotifications: false,
        trackData: false,
        techSupport: false,
        accountSpecialist: false,
        initialRender: false
    };

    static getDerivedStateFromProps(newProps, prevState) {
        if (prevState.initialRender) {
            return newProps
        }

        const data = newProps.profileData;

        if (!isEmpty(data)) {
            if (data) {
                return ({
                    newsletters: data.newsletters,
                    statNotifications: data.user.UserInputNotifications,
                    trackData: data.user.TrackingData,
                    techSupport: data.user.TechnicalSupport,
                    accountSpecialist: data.user.AccountSpecialist,
                    initialRender: true
                })
            } else {
                return ({
                    newsletters: data.newsletters,
                    statNotifications: false,
                    trackData: false,
                    techSupport: false,
                    accountSpecialist: false,
                    initialRender: true
                })
            }
        }
        return ({
            newsletters: false,
            statNotifications: false,
            trackData: false,
            techSupport: false,
            accountSpecialist: false,
            initialRender: false
        })
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.saveDataSettings(values);
            }
        });
    };

    handleChangeNewsletters = e => this.setState({newsletters: e});

    handleChangeStatNotifications = e => this.setState({statNotifications: e});

    handleChangeTrackData = e => this.setState({trackData: e});

    handleChangeTechSupport = e => this.setState({techSupport: e});

    handleChangeAccountSpecialist = e => this.setState({accountSpecialist: e});

    render() {
        const {getFieldDecorator} = this.props.form;
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14}
        };

        return (
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

                <FormItem
                    label={"Newsletters:"}
                    extra={"We would like to keep you updated with the latest software updates and features available to\n" +
                    "you, If you decide to not subscribe you may miss on important features and announcements."}
                    {...formItemLayout}>
                    {getFieldDecorator("newsletters", {
                        initialValue: this.state.newsletters,
                    })(
                        <Switch checked={this.state.newsletters} onChange={this.handleChangeNewsletters}
                                style={{marginRight: '5px'}}/>
                    )}
                </FormItem>

                <br/>

                <FormItem
                    label={"New Users Counter:"}
                    extra={"If allowed we will send you the number of new user records your assistants " +
                    "have stored through email. How often you will receive this is defined in the assistant settings"}
                    {...formItemLayout}>
                    {getFieldDecorator("statNotifications", {
                        initialValue: this.state.statNotifications,
                    })(
                        <Switch checked={this.state.statNotifications} onChange={this.handleChangeStatNotifications}
                                style={{marginRight: '5px'}}/>
                    )}
                </FormItem>

                <br/>

                <strong>Erasing data</strong>
                <p>If you decide to stop using our platform, we will simply delete
                    your information after a year of inactivity.</p>

                <br/>

                <FormItem
                    label={"Tracking Data:"}
                    extra={"We do not in any way track your information for marketing purposes. However we would recommend " +
                    "allowing us to contact you if we see that there are ways we could enhance your bot or use of our software."}
                    {...formItemLayout}>
                    {getFieldDecorator("trackData", {
                        initialValue: this.state.trackData,
                    })(
                        <Switch checked={this.state.trackData} onChange={this.handleChangeTrackData}
                                style={{marginRight: '5px'}}/>
                    )}
                </FormItem>

                <br/>

                <FormItem
                    label={"Technical Support:"}
                    extra={"Let our team view your errors and problems in order for us to solve your issues."}
                    {...formItemLayout}>
                    {getFieldDecorator("techSupport", {
                        initialValue: this.state.techSupport,
                    })(
                        <Switch checked={this.state.techSupport} onChange={this.handleChangeTechSupport}
                                style={{marginRight: '5px'}}/>
                    )}
                </FormItem>

                <br/>

                <FormItem
                    label={"Account Specialist:"}
                    extra={"Let our team contact you to help make recommendations as to how you can make your bots more " +
                    "successful and ways to collect more valuable data. If you don't have a sales specialist, we recommend " +
                    "you enable this so we can help you make the most of our software."}
                    {...formItemLayout}>
                    {getFieldDecorator("accountSpecialist", {
                        initialValue: this.state.accountSpecialist,
                    })(
                        <Switch checked={this.state.accountSpecialist} onChange={this.handleChangeAccountSpecialist}
                                style={{marginRight: '5px'}}/>
                    )}
                </FormItem>

                <br/>

                <div style={{textAlign: "center", marginBottom: "25px"}}><Button htmlType={"submit"}
                                                                                 className={"ant-btn-primary"}>Update</Button>
                </div>
            </Form>
        )
    }
}

export default Form.create()(DataSettings)