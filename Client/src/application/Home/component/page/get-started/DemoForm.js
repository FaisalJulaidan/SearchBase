import React from 'react'
import styles from "./demo-form.module.css";
import {connect} from 'react-redux';
import {Form, Input, Select, Button, Checkbox, Icon} from 'antd';
import {authActions} from '../../../../../store/actions/index';

class DemoForm extends React.Component {

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFieldsAndScroll((err, values) => {
            if (!err) {
                let {name, email, companyName, phone, crm, newsLetter} = values;
                this.props.dispatch(authActions.demoRequest(name, email, companyName, phone, crm, newsLetter));
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;

        return (
            <Form onSubmit={this.handleSubmit}>
                <Form.Item label="Full Name" className={styles.label}>
                    {getFieldDecorator('name', {
                        rules: [{required: true, message: 'Please input your full name!'}],
                    })(<Input prefix={<Icon type="user" className={styles.icon}/>} placeholder="John Lennon"/>)}
                </Form.Item>
                <Form.Item label="E-mail" className={styles.label}>
                    {getFieldDecorator('email', {
                        rules: [
                            {
                                pattern: /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,16})+$/,
                                message: 'The input is not a valid E-mail!'
                            },
                            {required: true, message: 'Please input your E-mail!'}
                        ],
                    })(<Input prefix={<Icon type="mail" className={styles.icon}/>} placeholder="example@mail.com"/>)}
                </Form.Item>
                <Form.Item label="Company Name" className={styles.label}>
                    {getFieldDecorator('companyName', {
                        rules: [{required: true, message: 'Please input your company name!'}],
                    })(<Input prefix={<Icon type="home" className={styles.icon}/>} placeholder="Your company name"/>)}
                </Form.Item>
                <Form.Item label="Phone Number" className={styles.label}>
                    {getFieldDecorator('phone', {
                        rules: [{
                            pattern: /^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$/,
                            message: 'The input is not a valid phone number.'
                        }, {
                            required: true,
                            message: 'Please input your phone number!'
                        }],
                    })(<Input prefix={<Icon type="phone" className={styles.icon}/>} placeholder="+123456789"/>)}
                </Form.Item>
                <Form.Item label="CRM Type" className={styles.label}>
                    {getFieldDecorator('crm', {
                        initialValue: 'bullhorn',
                        rules: [{required: true, message: 'Please select your desired CRM.'}],
                    })(
                        <Select>
                            <Select.Option value="adapt">Adapt</Select.Option>
                            <Select.Option value="bullhorn">Bullhorn</Select.Option>
                            <Select.Option value="rdb-pro-net">RDB Pro Net</Select.Option>
                            <Select.Option value="microdec">Microdec</Select.Option>
                            <Select.Option value="job-diva">JobDiva</Select.Option>
                            <Select.Option value="job-adder">JobAdder</Select.Option>
                            <Select.Option value="vincere">Vincere</Select.Option>
                            <Select.Option value="greenh-ouse">Greenhouse</Select.Option>
                            <Select.Option value="eploy">Eploy</Select.Option>
                            <Select.Option value="zoho">Zoho</Select.Option>
                            <Select.Option value="mercury-xrm">Mercury Xrm</Select.Option>
                            <Select.Option value="job-science">Job Science</Select.Option>
                            <Select.Option value="other">Other</Select.Option>
                        </Select>,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('newsLetter', {
                        initialValue: true,
                    })(
                        <Checkbox defaultChecked className={styles.checkbox}>
                            Subscribe to newsletters
                        </Checkbox>
                    )}
                </Form.Item>
                <Form.Item>
                    <Button loading={this.props.isRequestingDemo} type="primary" htmlType="submit" block>
                        Submit
                    </Button>
                </Form.Item>
            </Form>
        );
    }
}

function mapStateToProps(state) {
    return {
        isRequestingDemo: state.auth.isRequestingDemo,
    };
}

export default connect(mapStateToProps)(Form.create({name: 'demo'})(DemoForm));