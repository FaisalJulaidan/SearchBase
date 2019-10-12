import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {CardElement, injectStripe} from 'react-stripe-elements';
import {Form, Icon, Input,Button} from 'antd';
import styles from "./payment-form.module.css";

const FormItem = Form.Item;

class PaymentForm extends Component {

    stripeCardElementStyle= {
        base: {
            fontSize: '15px',
            color: 'rgba(0, 0, 0, 0.65)',
            letterSpacing: 'normal',
            lineHeight: '1.5em',
            '::placeholder': {
                color: 'rgba(0, 0, 0, 0.25)',
            }
        },
        invalid: {
            color: '#f5222d',
        },
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <Form onSubmit={this.handleSubmit} layout={'horizontal'}>
                <FormItem label="Email" className={styles.form_item}>
                    {getFieldDecorator('email', {
                        initialValue: this.props.email,
                        rules: [
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
                <FormItem label={'Card information'} className={styles.form_item}>
                    {getFieldDecorator('card', {})(
                        <CardElement className={styles.card_input} style={this.stripeCardElementStyle}/>
                    )}
                </FormItem>
                <FormItem  label={'Name on card'} className={styles.form_item}>
                    {getFieldDecorator('card_owner', {})(
                        <Input prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Name on card"/>
                    )}
                </FormItem>
                <FormItem  label={'country or region'} className={styles.form_item}>
                    {getFieldDecorator('country', {})(
                        <Input prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Country or region"/>
                    )}
                </FormItem>
                <Form.Item>
                    <Button loading={this.props.isRequestingDemo} type="primary" htmlType="submit" block>
                        Subscribe
                    </Button>
                </Form.Item>
            </Form>
        );
    }
}

PaymentForm.propTypes = {
    email: PropTypes.string,
};

export default injectStripe(Form.create()(PaymentForm));