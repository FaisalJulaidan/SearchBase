import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {CardElement, injectStripe} from 'react-stripe-elements';
import {Form, Icon, Input, Button} from 'antd';
import styles from "./payment-form.module.css";
import pricingJSON from "../pricing/pricing";

const FormItem = Form.Item;

class PaymentForm extends Component {

    componentDidMount() {
        const found = pricingJSON.some(plan => plan.id === this.props.planID);
        if (!found) {
            this.setState({planID: pricingJSON[0].id})
        } else {
            this.setState({planID: this.props.planID})
        }
    }

    state={
        planID: pricingJSON[0].id,
    };

    stripeCardElementStyle = {
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

        const plan = pricingJSON.find(plan => {
            if (plan.id === this.state.planID)
                return plan;
        });

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
                    {getFieldDecorator('card')(
                        <CardElement className={styles.card_input} style={this.stripeCardElementStyle}/>
                    )}
                </FormItem>
                <FormItem label={'Name on card'} className={styles.form_item}>
                    {getFieldDecorator('card_owner', {
                        rules: [{required: true, message: 'Please input card owner\'s name!'}],
                    })(
                        <Input prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Name on card"/>
                    )}
                </FormItem>
                <Button className={styles.button} loading={this.props.isRequestingDemo} type="primary" htmlType="submit" block>
                    Pay £{plan.price}
                </Button>
            </Form>
        );
    }
}

PaymentForm.propTypes = {
    planID: PropTypes.string.isRequired,
    email: PropTypes.string,
};

export default injectStripe(Form.create()(PaymentForm));