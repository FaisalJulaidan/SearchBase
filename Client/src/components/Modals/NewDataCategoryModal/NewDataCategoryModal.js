import React, {Component} from 'react';

import {Form, Input, Modal, Button} from 'antd';
import store from '../../../store/store';

const FormItem = Form.Item;
const layout = {
    labelCol: {span: 6},
    wrapperCol: {span: 14}
};

class NewDataCategoryModal extends Component {

    state = {

    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);

            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        return (
            <Modal width={500}
                   style={{ top: 70 }}
                   title="Add New Data Category"
                   visible={this.props.newAutoPilotModalVisible}
                   onCancel={this.props.closeEditAutoPilotModal}
                   destroyOnClose={true}
                   footer={null}
            >
                <Form layout='horizontal'
                      onSubmit={this.handleSubmit}>
                    <FormItem label="Name"
                              {...layout}>
                        {getFieldDecorator('name', {
                            rules: [{
                                required: true,
                                message: "Please choose a name",
                            }],
                        })(
                            <Input type="text" placeholder="Ex: Job Titles"/>
                        )}
                    </FormItem>
                    <FormItem {...layout}>
                        <Button type="primary" htmlType="submit">Create</Button>
                    </FormItem>
                </Form>

            </Modal>
        );
    }
}


export default Form.create()(NewDataCategoryModal);
