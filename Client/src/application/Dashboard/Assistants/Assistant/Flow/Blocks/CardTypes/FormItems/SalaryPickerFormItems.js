import React from 'react';
import { Radio, Select, Spin } from 'antd';

export * from './MinMaxSalaryFormItem';
const Option = Select.Option;

export const DefualtCurrencyFormItem = ({ FormItem, layout, getFieldDecorator, currencyCodes, block }) => (
    <FormItem label="Defualt Currency" {...layout}>
        {
            currencyCodes && currencyCodes[0] ?
                getFieldDecorator('defualtCurrency', {
                    rules: [{
                        required: true,
                        message: 'Please select an action'
                    }]
                })(
                    <Select placeholder="Select the defualt currency">
                        {
                            currencyCodes.map((currencyCode, i) =>
                                <Option key={i} value={currencyCode}>{currencyCode}</Option>)
                        }
                    </Select>
                )
                : <Spin><Select placeholder="Select the defualt currency"></Select></Spin>
        }
    </FormItem>
);

export const PayPeriodFormItem = ({ FormItem, layout, getFieldDecorator }) => (
    <FormItem label="Pay Period" {...layout}>
        {getFieldDecorator('payPeriod')(
            <Radio.Group>
                <Radio value="Annually">Annually</Radio>
                <Radio value="Daily">Daily</Radio>
            </Radio.Group>
        )}
    </FormItem>
);
