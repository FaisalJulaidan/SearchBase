import React from 'react';
import { Radio, Select, Spin } from 'antd';

export * from './MinMaxSalaryFormItem';
const Option = Select.Option;

export const DefualtCurrencyFormItem = ({ FormItem, layout, getFieldDecorator, currencyCodes, block }) => (
    <FormItem label="Currency" {...layout}>
        {
            currencyCodes && currencyCodes[0] ?
                getFieldDecorator('currency', {
                    initialValue: block.Content.currency,
                    rules: [{
                        required: true,
                        message: 'Please select currency'
                    }]
                })(
                    <Select placeholder="Select the currency">
                        {
                            currencyCodes.map((currencyCode, i) =>
                                <Option key={i} value={currencyCode}>{currencyCode}</Option>)
                        }
                    </Select>
                )
                : <Spin><Select placeholder="Select the currency"></Select></Spin>
        }
    </FormItem>
);

export const PayPeriodFormItem = ({ FormItem, layout, getFieldDecorator,block }) => (
    <FormItem label="Pay Period" {...layout}>
        {getFieldDecorator('payPeriod', {
            initialValue: block.Content.period,
            rules: [{
                required: true,
                message: 'Please select pay period'
            }]
        })(
            <Radio.Group>
                <Radio value="Annually">Annually</Radio>
                <Radio value="Daily">Daily</Radio>
            </Radio.Group>
        )}
    </FormItem>
);
