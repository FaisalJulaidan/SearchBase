import React from "react";
import {Input, Form, message} from "antd";
import {assistantActions} from "../../../../../store/actions";

const FormItem = Form.Item;

class ProfileInput extends React.Component {


    render(){
        return (
        <FormItem
            label={this.props.title + ":"}
            extra={this.props.description}
            {...this.props.formItemLayout}>
            {this.props.getFieldDecorator(this.props.name, {
                rules: [this.props.rules],
            })(
                <Input type={this.props.type} checked={this.props.checked} name={this.props.name} onChange={this.props.handleChange} readOnly={this.props.readOnly}/>
            )}
        </FormItem>
        )
    }
}

ProfileInput.defaultProps = {
    type:"text",
    checked:false,
    rules:{required:false}
};

export default ProfileInput;