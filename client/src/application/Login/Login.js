import React from 'react';
import {connect} from 'react-redux';

import {authActions} from '../../store/actions/index';
import styles from './Login.module.less';
import './Login.less';

import {Button, Col, Form, Icon, Input, Row, Spin} from 'antd';


const FormItem = Form.Item;
class Login extends React.Component {

    state = {
        isLoggin: false
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                //this.setState({isLoggin: true});
                console.log('Received values of form: ', values);
                this.props.dispatch(authActions.login(values.email, values.password));
            }
        });
    };

    handleLogout = () => {
        this.props.dispatch(authActions.logout());
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <div className={styles.LoginBackground}>
                <div className={[styles.LoginPanel, styles.fadeIn].join(' ')}>
                    <Spin spinning={this.state.isLoggin}>
                        <Row type="flex" justify="center">
                            <Col>
                                <h1>Login Page</h1>
                            </Col>
                        </Row>

                        {/*<Row type="flex" justify="center">*/}
                            {/*<Col>*/}
                                {/*<img width={200}*/}
                                     {/*src="https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/authentication_fsn5.svg"*/}
                                     {/*alt=""/>*/}
                            {/*</Col>*/}
                        {/*</Row>*/}

                        <br/>

                        <Row type="flex" justify="center">
                            <Col>
                                <Form onSubmit={this.handleSubmit} layout={'horizontal'}>
                                    <FormItem>
                                        {getFieldDecorator('email', {
                                            rules: [{required: true, message: 'Please input your email!'}],
                                        })(
                                            <Input prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                                   placeholder="Email"/>
                                        )}
                                    </FormItem>
                                    <FormItem>
                                        {getFieldDecorator('password', {
                                            rules: [{required: true, message: 'Please input your Password!'}],
                                        })(
                                            <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                                   type="password"
                                                   placeholder="Password"/>
                                        )}
                                    </FormItem>
                                </Form>
                            </Col>
                        </Row>

                        <Row type="flex" justify="center" className={styles.LoginButton}>
                            <Col span={12}>
                                <Button type="primary" htmlType="submit"
                                        style={{width: '100%'}}
                                        onClick={this.handleSubmit}>
                                    Log in
                                </Button>
                            </Col>
                        </Row>
                        <br/>

                        <Row type="flex" justify="center">
                            <Col>
                                <a className="login-form-forgot" href="account/resetpassword">Forgot password?</a>
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
        isLoggingIn: state.auth.isLoggingIn
    };
}

const loginForm = Form.create()(Login);
export default connect(mapStateToProps)(loginForm);
