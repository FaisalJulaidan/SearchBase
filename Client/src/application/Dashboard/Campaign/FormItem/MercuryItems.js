import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Form, Input} from 'antd';
import Item from "../../Marketplace/Item/Item";

class MercuryItems extends Component {
    render() {
        const {form} = this.props;
        const {getFieldDecorator} = form;
        return (
            <>
                <Form.Item label={"Mercury corresponding item"}>
                    {getFieldDecorator("test", {
                        rules: [{
                            whitespace: true,
                            required: true,
                            message: "This input is only for test"
                        }],
                    })(
                        <Input placeholder={"This input is only for test (Mercury)"}/>
                    )}
                </Form.Item>
            </>
        );
    }
}

MercuryItems.propTypes = {
    form: PropTypes.any.isRequired
};

export default MercuryItems;