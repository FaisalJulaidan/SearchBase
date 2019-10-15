import { Input } from 'antd';
import React, { Component } from 'react';

export class MinMaxSalaryFormItem extends Component {

    state = {
        minMaxValidateStatus: '',
        errorMsg: ''
    };

    componentDidMount() {
        this.props.onRef(this);

        this.props.form.setFieldsValue({
            minSalary: this.props.block.Content.min || undefined,
            maxSalary: this.props.block.Content.max || undefined
        });
    }

    componentWillUnmount() {
        this.props.onRef(undefined);
    }

    checkFields = () => new Promise(res => {
        this.props.form.validateFields(['minSalary', 'maxSalary'], (err, val) => {
            if (val.minSalary === undefined || !val.maxSalary === undefined)
                this.setState({
                    minMaxValidateStatus: 'error',
                    errorMsg: 'Fields are required!'
                }, () => res(false));
            else if (!val.minSalary || !val.maxSalary) {
                // sometime there are an error can be happended
                // when we change the form fields couple of times
                this.setState({
                    minMaxValidateStatus: 'error',
                    errorMsg: 'Re-enter  the fields'
                }, () => res(false));
            } else
                return res(true);
        });
    });

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
                          className={'SalaryPicker'}
                          help={this.state.errorMsg}
                          extra="This will be converated to be shown in the chatbot as slider"
                          {...layout}>
                    <Input.Group compact>
                        <Input onChange={(num) => this.validateFields(num, 'minSalary')}
                               defaultValue={this.props.block.Content.min || undefined}
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
                               defaultValue={this.props.block.Content.max || undefined}
                               style={{ width: 'calc(50% - 0px)', textAlign: 'center', borderLeft: 0 }}
                               placeholder="Maximum"/>
                    </Input.Group>
                </FormItem>
            </div>
        );
    }
}

