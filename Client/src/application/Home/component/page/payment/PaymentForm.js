import React, {Component} from 'react';
import {CardElement, injectStripe} from 'react-stripe-elements';

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

export default injectStripe(PaymentForm);