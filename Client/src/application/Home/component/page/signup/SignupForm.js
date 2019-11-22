import React from 'react';
import {connect} from 'react-redux';
import styles from './signup-form.module.css'
import momenttz from 'moment-timezone'
import {Form, Icon, Input, Select, Checkbox,Button} from 'antd';
import {Link,withRouter} from "react-router-dom";

import {authActions} from '../../../../../store/actions/index';

const FormItem = Form.Item;
const {Option} = Select;


const selectBeforeURL = (
    <Select defaultValue="http://" style={{width: 85}}>
        <Option value="http://">http://</Option>
        <Option value="https://">https://</Option>
    </Select>
);

class SignupForm extends React.Component {

    state = {
        confirmDirty: false,
    };

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.isSigningUp && (this.props.errorMsg === null)) {
            this.props.history.push('/login');
        }
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                values.timeZone = momenttz.tz.guess();
                // console.log('Received values of form: ', values);
                this.props.dispatch(authActions.signup(values));
            }
        });
    };

    handleConfirmBlur = (e) => {
        const value = e.target.value;
        this.setState({confirmDirty: this.state.confirmDirty || !!value});
    };

    compareToFirstPassword = (rule, value, callback) => {
        const form = this.props.form;
        if (value && value !== form.getFieldValue('password')) {
            callback('The two passwords are inconsistent!');
        } else {
            callback();
        }
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <Form onSubmit={this.handleSubmit} layout={'horizontal'}>

                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('companyName', {
                        rules: [{whitespace: true, required: true, message: 'Please input your company name!'}],
                    })(
                        <Input prefix={<Icon type="home" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Company Name"/>
                    )}
                </FormItem>


                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('websiteURL', {
                        rules: [{whitespace: true, required: true, message: 'Please input company website URL!'},
                            {
                                pattern: /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,16}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/,
                                message: 'Please, enter a valid URL'
                            }],
                    })(
                        <Input prefix={<Icon type="global" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Website URL" addonBefore={selectBeforeURL}/>
                    )}
                </FormItem>

                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('firstName', {
                        rules: [{whitespace: true, required: true, message: 'Please input your first name!'}],
                    })(
                        <Input prefix={<Icon type="idcard" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="First Name "/>
                    )}
                </FormItem>

                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('lastName', {
                        rules: [{whitespace: true, required: true, message: 'Please input your last name!'}],
                    })(
                        <Input prefix={<Icon type="idcard" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Last Name "/>
                    )}
                </FormItem>

                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('telephone', {
                        rules: [
                            {
                                whitespace: true,
                                pattern: /^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$/,
                                message: 'Sorry, use a valid number'
                            }
                        ],
                    })(
                        <Input prefix={<Icon type="phone" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Telephone"/>
                    )}
                </FormItem>


                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('email', {
                        rules: [
                            {whitespace: true, required: true, message: 'Please input your email!'},
                            {
                                pattern: "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\\])",
                                message: 'Sorry, use a valid email'
                            }
                        ],
                    })(
                        <Input prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Email"/>
                    )}
                </FormItem>


                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('password', {
                        rules: [
                            {whitespace: true, required: true, message: 'Please input your Password!'},
                            {validator: this.validateToNextPassword},
                            {pattern: /^.{6,}$/, message: 'Minimum is 6 characters'}
                        ],
                    })(
                        <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               type="password"
                               placeholder="Password"/>
                    )}
                </FormItem>

                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('confirm', {
                        rules: [
                            {whitespace: true, required: true, message: 'Please confirm your Password!'},
                            {validator: this.compareToFirstPassword}
                        ],
                    })(
                        <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               type="password"
                               placeholder="Password"
                               onBlur={this.handleConfirmBlur}/>
                    )}
                </FormItem>

                <Form.Item>
                    {getFieldDecorator('agreement', {
                        rules: [{required: true, message: 'You must agree to the terms & privacy policy'}],
                    })(
                        <Checkbox className={styles.checkbox}>I have read the <Link className={styles.link} to="/terms">terms</Link> & <Link
                            className={styles.link} to="/privacy">privacy
                            policy</Link></Checkbox>
                    )}
                </Form.Item>
                <Form.Item className={styles.SignupFormItem}>
                    <Button type="primary" htmlType="submit" block className={styles.submit}>
                        Sign up
                    </Button>
                </Form.Item>


            </Form>
        );
    }
}

function mapStateToProps(state) {
    return {
        isSigningUp: state.auth.isSigningUp,
        errorMsg: state.auth.errorMsg
    };
}

export default connect(mapStateToProps)(Form.create()(withRouter(SignupForm)));