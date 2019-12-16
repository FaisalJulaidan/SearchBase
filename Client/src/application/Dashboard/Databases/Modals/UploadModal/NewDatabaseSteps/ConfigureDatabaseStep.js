import {Form, Input, Select} from "antd";
import React, {Component} from 'react'
import {getLink} from "helpers";

const FormItem = Form.Item;
const Option = Select.Option;

class ConfigureDatabaseStep extends Component {


    checkName = (rule, value, callback) => {
        if (!this.props.isDatabaseNameValid(value)) {
            callback('Database name already exists. Choose another one, please!');
        } else {
            callback();
        }
    };



    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;
        const {databaseOptions} = this.props;

        return (
            <div>
                <div style={{textAlign: 'center'}}>
                    <img src={"/images/undraw/setup.svg"}
                         alt="Upload Data Iamge"
                         style={{height: 150, marginBottom: 10}}/>
                </div>
                <Form layout='horizontal'>
                    <FormItem label="Database Name"
                              extra="Enter unique name for your database"
                              {...formItemLayout}>
                        {getFieldDecorator('databaseName', {
                            initialValue: this.props.databaseConfiguration.databaseName,
                            rules: [
                                {required: true, message: 'Please input your database name'},
                                {validator: this.checkName}
                                ],
                        })(
                            <Input placeholder="Ex: London candidates, Jobs in Europe, etc..."/>
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
                            <Select placeholder="Please select type" loading={!(!!databaseOptions)}>
                                {
                                    databaseOptions ?
                                        databaseOptions.types.map((type, key) =>
                                            <Option key={key} value={type}>{type}</Option>)
                                        : null
                                }
                            </Select>
                        )}
                    </FormItem>
                </Form>
            </div>
        )
    }
}

export default Form.create()(ConfigureDatabaseStep);




