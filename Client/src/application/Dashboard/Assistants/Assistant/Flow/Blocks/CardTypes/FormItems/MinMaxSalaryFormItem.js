import { Input } from 'antd';
import React, { Component } from 'react';

export class MinMaxSalaryFormItem extends Component {

    state = {
        minMaxValidateStatus: '',
        errorMsg: ''
    };

    validateFields = (event, key) => {
        let maxSalary, minSalary;
        let value = maxSalary = minSalary = event.target.value;

        if (value) {
            if (key === 'maxSalary') {
                this.props.form.validateFields(['minSalary'],
                    (err, fields) => {
                        if (+maxSalary <= +fields.minSalary) {
                            this.props.form.setFieldsValue({ [key]: null });
                            this.setState({
                                minMaxValidateStatus: 'error',
                                errorMsg: 'Max should be greater than min!'
                            });
                        } else {
                            this.props.form.setFieldsValue({ [key]: value });
                            this.setState({
                                minMaxValidateStatus: 'success',
                                errorMsg: null
                            });
                        }
                    }
                );
            } else {
                this.props.form.validateFields(['maxSalary'],
                    (err, fields) => {
                        if (+minSalary >= +fields.maxSalary) {
                            this.props.form.setFieldsValue({ [key]: null });
                            this.setState({
                                minMaxValidateStatus: 'error',
                                errorMsg: 'Min should be less than max!'
                            });
                        } else {
                            this.props.form.setFieldsValue({ [key]: value });
                            this.setState({
                                minMaxValidateStatus: 'success',
                                errorMsg: null
                            });
                        }
                    }
                );
            }
        } else {
            this.props.form.setFieldsValue({ [key]: null });
            this.setState({
                minMaxValidateStatus: 'error',
                errorMsg: 'Min and max are requried!'
            });
        }
    };


    render() {
        const { FormItem, layout, getFieldDecorator } = this.props;
        return (
            <div>
                <FormItem>{getFieldDecorator('minSalary')(<></>)}</FormItem>
                <FormItem>{getFieldDecorator('maxSalary')(<></>)}</FormItem>

                <FormItem validateStatus={this.state.minMaxValidateStatus}
                          label="Min - Max Salary"
                          help={this.state.errorMsg}
                          {...layout}>
                    <Input.Group compact>
                        <Input onChange={(num) => this.validateFields(num, 'minSalary')}
                               style={{ width: 'calc(50% - 30px)', textAlign: 'center' }}
                               placeholder="Minimum"/>
                        <Input
                            style={{
                                width: 30,
                                borderLeft: 0,
                                pointerEvents: 'none',
                                backgroundColor: '#fff'
                            }}
                            placeholder="~"
                            disabled
                        />

                        <Input onChange={(num) => this.validateFields(num, 'maxSalary')}
                               style={{ width: 'calc(50% - 0px)', textAlign: 'center', borderLeft: 0 }}
                               placeholder="Maximum"/>
                    </Input.Group>
                </FormItem>
            </div>
        );
    }
}

