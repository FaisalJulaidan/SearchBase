import React from 'react';
import {connect} from 'react-redux';

import {authActions} from '../../store/actions/index';
import styles from './Login.module.less';

import {Button, Col, Form, Icon, Input, Row, Spin} from 'antd';
import {Link} from "react-router-dom";

const FormItem = Form.Item;
class Login extends React.Component {

    constructor(props) {
        super(props);
        this.handleEnter = this.handleEnter.bind(this);
    }

    handleEnter = e => e.keyCode === 13 ? this.handleSubmit() : null;

    componentDidMount() {
        document.addEventListener("keydown", this.handleEnter, false);
    }

    componentWillUnmount() {
        document.removeEventListener("keydown", this.handleEnter, false);
    }

    handleSubmit = (e) => {
        if (e)
            e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {

                let prevPath = this.props.history.location.state?.from.pathname || null;

                // prevPath has to have /dashboard keyword if not make it null
                if (prevPath?.indexOf('/dashboard') < -1)
                    prevPath = null;

                this.props.dispatch(authActions.login(values.email, values.password, prevPath));
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <div className={styles.LoginBackground}>
                <div className={[styles.LoginPanel, styles.fadeIn].join(' ')}>
                    <Spin spinning={this.props.isLoggingIn}>
                        <Row type="flex" justify="center">
                            <Col>
                                <h1>Login</h1>
                            </Col>
                        </Row>

                        <br/>

                        <Row type="flex" justify="center">
                            <Col>
                                <Form onSubmit={this.handleSubmit} layout={'horizontal'}>
                                    <FormItem className={styles.LoginFormItem}>
                                        {getFieldDecorator('email', {
                                            rules: [{required: true, message: 'Please input your email!'}],
                                        })(
                                            <Input prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                                                   placeholder="Email"/>
                                        )}
                                    </FormItem>
                                    <FormItem className={styles.LoginFormItem}>
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
                                <Link style={{color: "#9254de"}} to="/forget_password">Forgot password?</Link>
                            </Col>
                        </Row>

                        {/*<Row type="flex" justify="center">*/}
                            {/*<Col>*/}
                                {/*<Link style={{color: "#9254de"}} to="/signup">Don't have an account?</Link>*/}
                            {/*</Col>*/}
                        {/*</Row>*/}
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
