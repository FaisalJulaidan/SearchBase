import { Input } from 'antd';
import React from 'react';

const { TextArea } = Input;

export const RawTextFormItem = ({ FormItem, layout, getFieldDecorator, block, placeholder }) => (
    <FormItem label="Raw Text"
              extra="This message will displayed straight after the previous block"
              {...layout}>
        {getFieldDecorator('rawText', {
            initialValue: block.Content.text ? block.Content.text : undefined,
            rules: [{
                required: true,
                message: 'Please input raw text field'
            }]
        })(
            <TextArea placeholder={placeholder} autosize={{ minRows: 2, maxRows: 6 }}/>
        )}
    </FormItem>
);
