import {Form, Input, Select} from "antd";
import React, {Component} from 'react'
import "./UploadDatabaseStep/UploadDatabaseStep.less"

const FormItem = Form.Item;
const Option = Select.Option;

class ConfigureDatabaseStep extends Component {
    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;

        return (
            <div>
                <div style={{textAlign: 'center'}}>
                    <img
                        src="https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/setup_wizard_r6mr.svg"
                        alt="Upload Data Iamge"
                        style={{height: 150, marginBottom: 10}}/>
                </div>
                <Form layout='horizontal'>
                    <FormItem label="Database Name"
                              extra="Enter unique name for your database"
                              {...formItemLayout}>
                        {getFieldDecorator('databaseName', {
                            initialValue: this.props.databaseConfiguration.databaseName,
                            rules: [{
                                required: true,
                                message: 'Please input your assistant name',
                            }],
                        })(
                            <Input placeholder="Ex: London candidates, Jobs in europ, etc..."/>
                        )}
                    </FormItem>

                    <FormItem label="Database Type"
                              extra="Select one of the supported types"
                              {...formItemLayout}>
                        {getFieldDecorator('databaseType', {
                            initialValue: this.props.databaseConfiguration.databaseType,
                            rules: [{
                                required: true,
                                message: 'Please input your assistant name',
                            }],
                        })(
                            <Select placeholder="Please select type">
                                <Option value="candidate">Candidate</Option>
                                <Option value="client">Client</Option>
                            </Select>
                        )}
                    </FormItem>
                </Form>
            </div>
        )
    }
}

export default Form.create()(ConfigureDatabaseStep);




