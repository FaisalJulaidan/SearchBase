import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {CardElement, injectStripe} from 'react-stripe-elements';
import {Form} from 'antd';

class PaymentForm extends Component {


    render() {
        return (
            <div>
                <p>Would you like to complete the purchase?</p>
                <CardElement style={{base: {fontSize: '18px'}}} />
                <button onClick={this.submit}>Purchase</button>
            </div>
        );
    }
}

PaymentForm.propTypes = {};

export default injectStripe(PaymentForm);