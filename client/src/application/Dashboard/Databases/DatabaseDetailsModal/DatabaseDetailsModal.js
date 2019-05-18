import {Button, Modal, Form, Input, Select} from 'antd';

import React, {Component} from 'react';

const FormItem = Form.Item;
const Option = Select.Option;

class DatabaseDetailsModal extends Component {

    constructor(props) {
        super(props);
    }

    checkName = (rule, value, callback) => {
        if (!this.props.isDatabaseNameValid(value) && this.props.databaseInfo.Name !== value) {
            callback('Database name already exists. Choose another one, please!');
        } else {
            callback();
        }
    };

    handleSave = () => this.props.form.validateFields((errors, values) => {
        const {databaseInfo, updateDatabase, hideModal} = this.props;
        if (!errors){
            hideModal();
            return updateDatabase(values, databaseInfo.ID)
        }

    });

    render() {
        const {getFieldDecorator} = this.props.form;
        const {databaseInfo, databaseOptions} = this.props;
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };

        return (
            <Modal width={"60%"}
                   title="Update Database"
                   visible={this.props.visible}
                   onCancel={this.props.hideModal}
                   destroyOnClose={true}
                   footer={[
                       <Button key="cancel" onClick={this.props.hideModal}>Cancel</Button>,
                       <Button key="submit" type="primary" onClick={this.handleSave}>Save</Button>,
                   ]}>
                <Form layout='horizontal'>
                    <FormItem
                        label="Database Name"
                        extra="Enter unique name for your database"
                        {...formItemLayout}>
                        {
                            getFieldDecorator('databaseName', {
                                initialValue: databaseInfo?.Name,
                                rules: [
                                    {required: true, message: 'Please input your database name'},
                                    {validator: this.checkName},
                                    ],
                            })
                            (<Input placeholder="Ex: London candidates, Jobs in Europe, etc..."/>)
                        }
                    </FormItem>

                    <FormItem label="Database Type" extra="Select one of the supported types"
                              {...formItemLayout}>
                        {getFieldDecorator('databaseType', {
                            initialValue: databaseInfo?.Type?.name,
                            rules: [{
                                required: false,
                            }],
                        })(
                            <Select disabled={true} placeholder="Please select type" loading={!(!!databaseOptions)}>
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
