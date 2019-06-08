import React, {Component} from 'react';
import {connect} from 'react-redux';
import {store} from "store/store";

import {Button, Select, Form, Divider} from "antd";
import {assistantActions, crmActions} from "store/actions";
import {history} from "helpers";

const Option = Select.Option;


class Connections extends Component {


    render() {
        const {getFieldDecorator} = this.props.form;
        console.log(this.props.CRMsList);
        return (
            <>
                <Form layout='vertical' wrapperCol={{span: 12}}>

                    <h2> Basic Settings:</h2>
                    <Form.Item label="CRM">
                        {getFieldDecorator('crmID', {
                            rules: [{ required: true, message: 'Please select your gender!' }],
                        })(
                            <Select
                                placeholder="Select a option and change input text above"
                                onChange={this.handleSelectChange}
                            >
                                <Option value="male">male</Option>
                                {this.props.CRMsList.map(crm => {
                                    return <Option value="crm.ID">crm.Type</Option>
                                })}
                            </Select>,
                        )}
                    </Form.Item>



                    <Button type={'primary'} onClick={this.handleSave}>Save changes</Button>
                </Form>

            </>
        );
    }
}

function mapStateToProps(state) {
    return {};
}

export default connect(mapStateToProps)(Form.create()(Connections));