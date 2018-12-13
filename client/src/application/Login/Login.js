import React from 'react';
import {connect} from 'react-redux';

import {authActions} from '../../store/actions/index';
import styles from './Login.module.less';
import './Login.less';

import {Form, Icon, Input, Button} from 'antd';
import {Avatar} from 'antd';


const FormItem = Form.Item;
class Login extends React.Component {

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
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
            <div className={styles.Panel} style={{padding: 75, textAlign: 'center'}}>

                <Avatar size={128} icon="user" style={{marginBottom: 50}}/>

                <Form onSubmit={this.handleSubmit} className="login-form">
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
                            <Input prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>} type="password"
                                   placeholder="Password"/>
                        )}
                    </FormItem>
                    <FormItem>
                        <Button type="primary" htmlType="submit" className="login-form-button">
                            Log in
                        </Button>
                    </FormItem>
                </Form>
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
