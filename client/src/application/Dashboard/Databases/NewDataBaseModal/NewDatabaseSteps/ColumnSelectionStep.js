import {Form, Input, Select, Checkbox, Button, Divider} from "antd";
import NoticeIcon from 'ant-design-pro/lib/NoticeIcon';

import React, {Component} from 'react'
import "./UploadDatabaseStep/UploadDatabaseStep.less"

const FormItem = Form.Item;

class ColumnSelectionStep extends Component {
    state = {
        selectedColumns: [],
    };

    handleChange = selectedColumns => this.setState({selectedColumns: [...this.state.selectedColumns].concat(selectedColumns).unique()})


    handleRemove = removedColumn => setTimeout(() => this.setState({selectedColumns: this.state.selectedColumns.filter(selectedColumn => selectedColumn !== removedColumn)}
        , 100)
    );


    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };

        const {getFieldDecorator} = this.props.form;
        const {databaseOptions, databaseType} = this.props;
        const {selectedColumns} = this.state;
        const filteredOptions = this.props.excelFile.headers.filter(o => !selectedColumns.includes(o));

        return (
            <div>
                <div style={{textAlign: 'center'}}>
                    <img
                        src="https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/setup_wizard_r6mr.svg"
                        alt="Upload Data Image"
                        style={{height: 150, marginBottom: 10}}/>
                </div>
                <Form layout='horizontal'>
                    {
                        databaseOptions[databaseType].map((type, index) =>
                            <FormItem label={type.column} {...formItemLayout} key={index}>
                                {getFieldDecorator(type.column, {
                                    defaultValue: selectedColumns,
                                    rules: [{
                                        required: !type.nullable,
                                        message: 'This is required field',
                                    }],
                                })(
                                    <Select mode="multiple"
                                            placeholder="Select Column or Columns"
                                            onDeselect={this.handleRemove}
                                            onChange={this.handleChange}>
                                        {filteredOptions.map(item => (
                                            <Select.Option key={item} value={item}>
                                                {item}
                                            </Select.Option>
                                        ))}
                                    </Select>
                                )}
                            </FormItem>
                        )
                    }
                </Form>
            </div>
        )
    }
}

export default Form.create()(ColumnSelectionStep);

Array.prototype.unique = function () {
    let a = this.concat();
    for (let i = 0; i < a.length; ++i) {
        for (let j = i + 1; j < a.length; ++j) {
            if (a[i] === a[j])
                a.splice(j--, 1);
        }
    }
    return a;
};

