import React from 'react';
import PropTypes from "prop-types";
import {connect} from 'react-redux';
import styles from './signup-form-payment.module.css'
import momenttz from 'moment-timezone'
import {Form, Icon, Input, Select, Checkbox, Button} from 'antd';
import {Link, withRouter} from "react-router-dom";

import {authActions} from '../../../../../store/actions/index';
import pricingJSON from "../pricing/pricing";

const FormItem = Form.Item;
const {Option} = Select;


const selectBeforeURL = (
    <Select defaultValue="http://" style={{width: 85}}>
        <Option value="http://">http://</Option>
        <Option value="https://">https://</Option>
    </Select>
);

class SignupFormPayment extends React.Component {

    componentDidMount() {
        const found = pricingJSON.some(item => item.id === this.props?.plan);
        if (!found) {
            this.setState({plan: pricingJSON[0].id})
        } else {
            this.setState({plan: this.props.plan})
        }
    }


    state = {
        confirmDirty: false,
    };

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.isSigningUp && (this.props.errorMsg === null)) {
            this.props.onSignupSuccessful(this.state.plan,this.props.form.getFieldValue('email'));
        } else if (prevState.plan !== this.state.plan)
            this.props.history.push(`/order-plan?plan=${this.state.plan}`);
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                values.timeZone = momenttz.tz.guess();
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
                        rules: [{required: true, message: 'Please input your company name!'}],
                    })(
                        <Input prefix={<Icon type="home" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Company Name"/>
                    )}
                </FormItem>


                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('websiteURL', {
                        rules: [{required: true, message: 'Please input company website URL!'},
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
                            {
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
                            {required: true, message: 'Please input your email!'},
                            {
                                pattern: /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,16})+$/,
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
                            {required: true, message: 'Please input your Password!'},
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

                <FormItem className={styles.SignupFormItem}>
                    {getFieldDecorator('plan', {
                        initialValue: this.state.plan,
                        rules: [
                            {required: true, message: 'Please select a plan'},
                        ],
                    })(
                        <Select onSelect={(value) => {
                            this.setState({plan: value})
                        }}>
                            {
                                pricingJSON.map((plan) => {
                                    return (
                                        <Select.Option key={plan.id}>{plan.title}</Select.Option>
                                    );
                                })
                            }
                        </Select>
                    )}
                </FormItem>

                <Form.Item>
                    {getFieldDecorator('agreement', {
                        rules: [{required: true, message: 'You must agree to terms & privacy policy'}],
                    })(
                        <Checkbox className={styles.checkbox}>I have read the <Link className={styles.link}
                                                                                    to="/terms">terms</Link> & <Link
                            className={styles.link} to="/privacy">privacy
                            policy</Link></Checkbox>
                    )}
                </Form.Item>
                <Form.Item className={styles.SignupFormItem}>
                    <Button type="primary" htmlType="submit" block>Submit</Button>
                </Form.Item>
            </Form>
        );
    }
}

SignupFormPayment.propTypes = {
    plan: PropTypes.string,
    onSignupSuccessful: PropTypes.func.isRequired
};

function mapStateToProps(state) {
    return {
        isSigningUp: state.auth.isSigningUp,
        errorMsg: state.auth.errorMsg
    };
}

export default connect(mapStateToProps)(Form.create()(withRouter(SignupFormPayment)));