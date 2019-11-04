import React from 'react';
import {connect} from 'react-redux';
import {withRouter} from "react-router-dom";
import styles from './login-form.module.css'
import {Form, Icon, Input, Button} from 'antd';

import {authActions} from '../../../../../store/actions/index';

class LoginForm extends React.Component {

    handleSubmit = (e) => {
        if (e) e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                let from = this.props.history.location.state?.from || "";
                let prevPath = from?.pathname || "";
                if (prevPath) prevPath += from.search;

                // prevPath has to have /dashboard keyword if not make it null
                if (prevPath?.indexOf('/dashboard') < -1)
                    prevPath = null;

                this.props.dispatch(authActions.login(values.email, values.password, `successful-login?prevPath=${prevPath}`));
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <Form onSubmit={this.handleSubmit} className="login-form">
                <Form.Item className={styles.form_item}>
                    {getFieldDecorator('email', {
                        rules: [{required: true, message: 'Please input your Email!'}],
                    })(<Input prefix={<Icon type="mail" className={styles.icon}/>} placeholder="E-Mail"/>,)}
                </Form.Item>
                <Form.Item className={styles.form_item}>
                    {getFieldDecorator('password', {
                        rules: [{required: true, message: 'Please input your Password!'}],
                    })(<Input prefix={<Icon type="lock" className={styles.icon}/>}
                              type="password" placeholder="Password"/>)}
                </Form.Item>
                <Form.Item className={styles.form_item}>
                    <h1 className={styles.forgot_pass}>Forgot your <a href="/forget_password">password</a>?</h1>
                    <Button type="primary" htmlType="submit" block className={styles.submit}>
                        Log in
                    </Button>
                </Form.Item>
            </Form>
        );
    }
}

function mapStateToProps(state) {
    return {
        isLoggingIn: state.auth.isLoggingIn
    };
}

export default connect(mapStateToProps)(withRouter(Form.create()(LoginForm)));