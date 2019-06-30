import React from "react";
import {Button, Form, Icon, Input} from "antd";
import {successMessage} from "helpers";

const FormItem = Form.Item;

class TextWebLink extends React.Component {

    state = {
        output: ""
    };

    copyOutput = () => {
        const el = document.createElement('textarea');
        el.value = this.state.output;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
        successMessage("Copied");
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                // this.props.saveProfileDetails(values);
                this.setState({output: "*&&TEXT:" + values["text"] + "*&&LINK:http://" + values["link"] + "*&&END*"});
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        const formItemLayout = this.props.formLayout;

        return (
            <Form onSubmit={this.handleSubmit}>
                Generate a clickable link by filling the bellow boxes and then pasting the output in your questions.
                <br/><br/>
                <FormItem
                    label={"Text to Display"}
                    {...formItemLayout}>
                    {getFieldDecorator('text', {
                        rules: [
                            {required: true, message: 'Please type in the text to display!'},
                        ],
                    })(
                        <Input  prefix={<Icon type="font-size" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="Click me"/>
                    )}
                </FormItem>

                <FormItem
                    label={"Link:"}
                    {...formItemLayout}>
                    {getFieldDecorator('link', {
                        rules: [
                            {required: true, message: 'Please input the link!'},
                        ],
                    })(
                        <Input addonBefore="http://" prefix={<Icon type="link" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder="www.google.com"/>
                    )}
                </FormItem>
                <br/>

                <FormItem
                    label={"Output:"}
                    {...formItemLayout}>
                    {getFieldDecorator('output', {
                        initialValue: this.state.output
                    })(
                        <Input disabled={true} style={{cursor: "auto", color:"black"}}/>
                    )}
                </FormItem>
                <br/>

                <div style={{textAlign: "center", marginBottom: "25px"}}>
                    <Button htmlType={"button"} onClick={this.copyOutput} className={"ant-btn-primary"}
                    style={{marginRight:"7px"}}>Copy</Button>
                    <Button htmlType={"submit"} className={"ant-btn-primary"}>Generate Link</Button>
                </div>
            </Form>
        )
    }
}

export default Form.create()(TextWebLink);