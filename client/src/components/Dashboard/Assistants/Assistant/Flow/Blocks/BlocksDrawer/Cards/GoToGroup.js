import React, {Component} from 'react';
import {Button, Card, Form, Input, Select} from "antd";

const FormItem = Form.Item;
const Option = Select.Option;

class GoToGroup extends Component {

    render() {
        return (<Card
                title="Question"
                extra={<Button type="primary" icon="plus" onClick={this.props.onClose}>
                    Add Block</Button>}
                style={{width: '100%'}}>

                <Form layout='horizontal'>
                    <FormItem
                        label="Question"
                        {...this.props.layout}>
                        <Input placeholder="Ex: Where are you from?"/>
                    </FormItem>

                    <FormItem {...this.props.layout}
                              label="Validation">

                        <Select placeholder="Will validate the input">
                            <Option value="recruitment">Ignore</Option>
                            <Option value="Shopping">Email</Option>
                            <Option value="Sales">Full Name</Option>
                        </Select>
                    </FormItem>

                    <FormItem
                        label="After message"
                        {...this.props.layout}>
                        <Input placeholder="Ex: Your input is considered"/>
                    </FormItem>

                </Form>
            </Card>
        );
    }

}

export default GoToGroup;

