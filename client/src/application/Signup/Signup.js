import React from 'react';
import {connect} from 'react-redux';

import {authActions} from '../../store/actions/index';
import styles from './Signup.module.less';
import {Link} from 'react-router-dom';
import {Form, Input, Icon, Select, Row, Col, Checkbox, Button, Spin} from 'antd';

const FormItem = Form.Item;
const { Option } = Select;


const selectBeforeURL = (
    <Select defaultValue="http://" style={{ width: 85 }}>
        <Option value="http://">http://</Option>
        <Option value="https://">https://</Option>
    </Select>
);


class Signup extends React.Component {

    state = {
        confirmDirty: false,
        autoCompleteResult: [],
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                this.props.dispatch(authActions.signup(values));
            }
        });
    };

    handleConfirmBlur = (e) => {
        const value = e.target.value;
        this.setState({ confirmDirty: this.state.confirmDirty || !!value });
    };

    compareToFirstPassword = (rule, value, callback) => {
        const form = this.props.form;
        if (value && value !== form.getFieldValue('password')) {
            callback('Two passwords that you enter is inconsistent!');
        } else {
            callback();
        }
    };

    validateToNextPassword = (rule, value, callback) => {
        const form = this.props.form;
        if (value && this.state.confirmDirty) {
            form.validateFields(['confirm'], { force: true });
        }
        callback();
    };

    // handleLogout = () => {
    //     this.props.dispatch(authActions.logout());
    // };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <div className={styles.SignupBackground}>
                <div className={[styles.SignupPanel, styles.fadeIn].join(' ')}>
                    <Spin spinning={false}>
                        <Row type="flex" justify="center">
                            <Col>
                                <h1>Signup Page</h1>
                            </Col>
                        </Row>

                        <br/>


                        <Row type="flex" justify="center">
                            <Col>
                                <Form onSubmit={this.handleSubmit} layout={'horizontal'}>

                                    <FormItem className={styles.SignupFormItem}>
                                        {getFieldDecorator('companyName', {
                                            rules: [{required: true, message: 'Please input your company name!'}],
                                        })(
                                            <Input prefix={<Icon type="home" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                                   placeholder="Company Name"/>
                                        )}
                                    </FormItem>



                                    <FormItem className={styles.SignupFormItem}>
                                        {getFieldDecorator('websiteURL', {
                                            rules: [{required: true, message: 'Please input company website URL!'},
                                                {pattern: /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/,
                                                    message: 'Sorry, input a valid URL'}],
                                        })(
                                            <Input prefix={<Icon type="global" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                                   placeholder="Website URL" addonBefore={selectBeforeURL}/>
                                        )}
                                    </FormItem>

                                    <FormItem className={styles.SignupFormItem}>
                                        {getFieldDecorator('firstName', {
                                            rules: [{required: true, message: 'Please input your first name!'}],
                                        })(
                                            <Input prefix={<Icon type="idcard" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                                   placeholder="First Name "/>
                                        )}
                                    </FormItem>

                                    <FormItem className={styles.SignupFormItem}>
                                        {getFieldDecorator('lastName', {
                                            rules: [{required: true, message: 'Please input your last name!'}],
                                        })(
                                            <Input prefix={<Icon type="idcard" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                                   placeholder="Last Name "/>
                                        )}
                                    </FormItem>

                                    <FormItem className={styles.SignupFormItem}>
                                        {getFieldDecorator('telephone', {
                                            rules: [
                                                {pattern: /^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$/,
                                                    message: 'Sorry, use a valid number'}
                                            ],
                                        })(
                                            <Input prefix={<Icon type="phone" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                                   placeholder="Telephone"/>
                                        )}
                                    </FormItem>


                                    <FormItem className={styles.SignupFormItem}>
                                        {getFieldDecorator('email', {
                                            rules: [
                                                {required: true, message: 'Please input your email!'},
                                                {pattern: /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
                                                    message: 'Sorry, use a valid email'}
                                            ],
                                        })(
                                            <Input prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                                   placeholder="Email"/>
                                        )}
                                    </FormItem>


                                    <FormItem className={styles.SignupFormItem}>
                                        {getFieldDecorator('password', {
                                            rules: [
                                                {required: true, message: 'Please input your Password!'},
                                                {validator: this.validateToNextPassword}
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
                                                {required: true, message: 'Please confirm your Password!'},
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
                                            rules: [{required: true, message: 'Agree to our Terms & Privacy Policy first'}],
                                        })(
                                            <Checkbox>I have read the <a href="/privacy">Terms & Privacy Policy</a></Checkbox>
                                        )}
                                    </Form.Item>


                                </Form>
                            </Col>
                        </Row>

                        <Row type="flex" justify="center" className={styles.SignupButton}>
                            <Col span={12}>
                                <Button type="primary" htmlType="submit"
                                        style={{width: '100%'}}
                                        onClick={this.handleSubmit}>
                                    Create Account
                                </Button>
                            </Col>
                        </Row>
                        <br/>

                        <Row type="flex" justify="center">
                            <Col>
                                <Link to="/login">Already have an account?</Link>
                            </Col>
                        </Row>


                        <br/>
                    </Spin>
                </div>
            </div>
        );


    }
}

function mapStateToProps(state) {
    return {
        isSigningUp: state.auth.isSigningUp,
    };
}

const signupForm = Form.create()(Signup);
export default connect(mapStateToProps)(signupForm);
