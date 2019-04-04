import React from "react";
import {Button, Form, Input} from "antd";
import {isEmpty} from "lodash";

const FormItem = Form.Item;

class ProfileDetails extends React.Component {

    state= {
        name: "",
        email: "",
        companyName: ""
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.saveProfileDetails(values);
            }
        });
    };

    componentWillReceiveProps(nextProps){
        const data = nextProps.profileData;
        if(!isEmpty(data)){
            if(data.user && data.user.email !== this.state.email){
                this.setState({
                    name: data.user.Firstname + " " + data.user.Surname,
                    email: data.user.Email,
                    companyName: data.company.Name
                });
            }
        }
    }

    render() {
        const {getFieldDecorator} = this.props.form;

        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14}
        };

        return (
            <Form onSubmit={this.handleSubmit}>
                <FormItem
                    label={"Name:"}
                    extra={"Enter your name here"}
                    {...formItemLayout}>
                    {getFieldDecorator("name", {
                        initialValue: this.state.name,
                        rules: [{
                            required: true,
                            message: "Please enter your first and last name here"
                        }],
                    })(
                        <Input/>
                    )}
                </FormItem>

                <FormItem
                    label={"Email:"}
                    extra={"For your security we have temporarily disabled this box"}
                    {...formItemLayout}>
                    {getFieldDecorator("email", {
                        initialValue: this.state.email,
                        rules: [{
                            required: true,
                            message: "Please enter a valid email"
                        }],
                    })(
                        <Input disabled={true} readOnly={true}/>
                    )}
                </FormItem>

                <FormItem
                    label={"Company Name:"}
                    extra={"Enter your company name here"}
                    {...formItemLayout}>
                    {getFieldDecorator("companyName", {
                        initialValue: this.state.companyName,
                        rules: [{
                            required: true,
                            message: "Please enter your company name"
                        }],
                    })(
                        <Input/>
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

export default Form.create()(ProfileDetails)