import {Form, Input, Select, Checkbox, Button, Divider, Icon} from "antd";
import NoticeIcon from 'ant-design-pro/lib/NoticeIcon';

import React, {Component} from 'react'
import "./UploadDatabaseStep/UploadDatabaseStep.less"

const FormItem = Form.Item;
const Option = Select.Option;

class ColumnSelectionStep extends Component {
    state = {
        selectedColumns: [],
    };

    handleChange = selectedColumns => this.setState({selectedColumns: [...this.state.selectedColumns].concat(selectedColumns).unique()});
    handleRemove = removedColumn => setTimeout(() => this.setState({selectedColumns: this.state.selectedColumns.filter(selectedColumn => selectedColumn !== removedColumn)}), 100);

    validate = () => {
        const {form: {validateFields}, excelFile} = this.props;
        validateFields((errors, columns) => {
            // convert object to array of {ourColumn, excelColumn} pairs
            const me = this.props;
            columns = Object.keys(columns).map(key => {
                return {ourColumn: key, excelColumn: columns[key]};
            });
            // get columns which have mapped column with excelColumn
            const selectedColumns = columns.filter(column => !!column.excelColumn);

            let validRecords = [];
            let invalidRecords = [];

            // Definition
            // selectedColumns[]: {
            //     ourColumn: String,
            //     excelColumn: String[]
            // }

            // excel.data
            /*
            - - - - - - -
            -
            -

            | | | | => selcted columns
            --------
            | => validator
            I need to check all excel records for this specifc column
            & when i'm done push it the valid recrod

            N
            | | | |
            - - - -
            - * - -
            - - - -

            valid_records = []
            invalid_records = []

            loop => excel.data as user_record
                for (const selectedColum of selectedColumns){
                    const {ourColumn,excelColumn} = selectedColum;

                    type = databaseOptions[databaseType].find(type => type.column === ourColumn);
                    record[ourColumn] = validate_and_construct(type,[...excelColumn])
                }

                name = {
                    data:'hey',
                    messeage:null,
                    isValid:true
                }
                record['x'] = validate(type,[user_record.['m'],user_record.['n']])
                record['y'] = validate(user_record.['y'])
                record['z'] = validate(user_record.['z'])
                record['k'] = validate(user_record.['k'])

                loop in the record keys and check if record doens't have any invalid colum

                loop => record.keys as key
                    if(!recod[key].isValid)
                        return invalid_records.push(record)

                records.push(record)

             records: record[]
             record: {string: validate}[]
             validate: (string , string[])=> {
                data: string || number,
                message: string,
                isValid: boolean
             }


             */
            for (const selectedColumn of selectedColumns) {
                // find the validator from databaseOptions
                const columnValidator = me.databaseOptions[me.databaseType].find(type => type.column === selectedColumn.ourColumn);

                if (columnValidator.type.includes("VARCHAR")) {
                    // get number from varchar then validate string length
                    const string_length = /\(([^)]+)\)/.exec(columnValidator.type)[1];
                    for (const record of excelFile.data) {
                        let isValidRecord = false;
                        for (const excelColumn of selectedColumn.excelColumn) {
                            // because XLSX doesn't return the empty columns
                            if (record[excelColumn])
                                isValidRecord = record[excelColumn].length <= string_length;
                            else if (columnValidator.nullable)
                                isValidRecord = true;
                        }

                        if (isValidRecord) validRecords.push(record);
                        else invalidRecords.push({
                            record,
                            justification: `${selectedColumn.excelColumn} doesn't meet the validation of VARCHAR(${string_length})`
                        });
                    }
                }

                if (columnValidator.type === "FLOAT") {
                    for (const record of excelFile.data) {
                        let isValidRecord = false;

                        for (const excelColumn of selectedColumn.excelColumn) {
                            // because XLSX doesn't return the empty cells
                            if (record[excelColumn])
                                isValidRecord = isNaN(record[excelColumn]);
                            else
                                isValidRecord = false
                        }

                        if (isValidRecord) validRecords.push(record);
                        else invalidRecords.push({
                            record,
                            justification: `${selectedColumn.excelColumn} doesn't meet the validation of FLOAT`
                        });
                    }
                }

                if (columnValidator.type === "DATETIME") {
                    // Ask Faisal
                }
            }

            debugger

        });
    };

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
                                    type.column === "Currency" ?
                                        <Select key={index} placeholder="Please select currency">
                                            {databaseOptions.currencyCodes.map(
                                                (currencyCode, index) =>
                                                    <Option key={index} value={currencyCode}>{currencyCode}</Option>
                                            )}
                                        </Select> :

                                        <Select mode="multiple"
                                                placeholder="Select Column or Columns"
                                                onDeselect={this.handleRemove}
                                                onChange={this.handleChange}>
                                            {filteredOptions.map(item => (
                                                <Select.Option key={item} value={item}>{item}</Select.Option>
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

