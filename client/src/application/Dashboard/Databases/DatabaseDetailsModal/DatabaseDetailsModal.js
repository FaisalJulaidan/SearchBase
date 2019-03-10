import {Button, Divider, Modal, Steps, Spin, message, Form, Input, Switch, InputNumber, Slider, Select} from 'antd';

import React, {Component} from 'react';

const FormItem = Form.Item;
const Option = Select.Option;

class DatabaseDetailsModal extends Component {

    constructor(props) {
        super(props);
    }

    render() {

        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };


        const {getFieldDecorator, validateFields} = this.props.form;

        const {databaseInfo, databaseOptions, updateDatabase} = this.props;

        const handleSave = () => validateFields((errors, columns) => {
            if (!errors)
                return updateDatabase(columns)
        });

        return (
            <Modal width={"60%"}
                   title="Update Database"
                   visible={this.props.visible}
                   onCancel={this.props.hideModal}
                   destroyOnClose={true}
                   footer={[
                       <Button key="cancel" onClick={this.props.hideModal}>Cancel</Button>,
                       <Button key="submit" type="primary" onClick={handleSave}>Save</Button>,
                   ]}>
                <Form layout='horizontal'>
                    <FormItem
                        label="Database Name"
                        extra="Enter a name for your assistant to easily identify it in the dashboard"
                        {...formItemLayout}>
                        {
                            getFieldDecorator('databaseName', {
                                initialValue: databaseInfo?.Name,
                                rules: [{
                                    required: true,
                                    message: 'Please input your assistant name',
                                }],
                            })
                            (<Input placeholder="Ex: My first assistant, Sales Assistant"/>)
                        }
                    </FormItem>

                    <FormItem label="Database Type" extra="Select one of the supported types"
                              {...formItemLayout}>
                        {getFieldDecorator('databaseType', {
                            initialValue: databaseInfo?.Type?.name,
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
            </Modal>
        );
    }
}

export default Form.create()(DatabaseDetailsModal);