import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Form, Input} from 'antd';

class BullhornItems extends Component {
    render() {
        const {form} = this.props;
        const {getFieldDecorator} = form;
        return (
            <>
                <Form.Item label={"Bullhorn corresponding item"}>
                    {getFieldDecorator("test", {
                        rules: [{
                            whitespace: true,
                            required: true,
                            message: "This input is only for test"
                        }],
                    })(
                        <Input placeholder={"This input is only for test (Bullhorn)"}/>
                    )}
                </Form.Item>
            </>
        );
    }
}

BullhornItems.propTypes = {
    form: PropTypes.any.isRequired
};

export default BullhornItems;