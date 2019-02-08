import {Form, Input, Select, Checkbox, Button, Divider, Icon} from "antd";

import React, {Component} from 'react'
import "./UploadDatabaseStep/UploadDatabaseStep.less"

const FormItem = Form.Item;
const Option = Select.Option;


/**
 * Columns which have mapped with excelColumn
 @typedef SelectedColumn
 @type {object}
 @property {string} ourColumn - TSB colums naming.
 @property {string[]} excelColumn - Users' colums naming.
 */

/**
 * Columns which have mapped with excelColumn
 @typedef TSBcolumnOption
 @type {object}
 @property {string} column - the name of the column.
 @property {boolean} nullable - is nullable?.
 @property {string} type - type of column (VARCHAR(any) | FLOAT | DATETIME).
 */

/**
 * The returned object from validate_and_construct function
 @typedef ColumnValidator
 @type {object}
 @property {(string|number|null)} data - the record's data.
 @property {(string|null)} message - if not valid here will be a message.
 @property {boolean} isValid - to check if valid or not.
 */

/**
 * The constructed record before check if valid or not
 @typedef NewRecord
 @type {Object.<string, ColumnValidator>}
 */


class ColumnSelectionStep extends Component {
    state = {
        selectedColumns: [],
    };

    handleChange = selectedColumns => this.setState({selectedColumns: [...this.state.selectedColumns].concat(selectedColumns).unique()});
    handleRemove = removedColumn => setTimeout(() => this.setState({selectedColumns: this.state.selectedColumns.filter(selectedColumn => selectedColumn !== removedColumn)}), 100);

    /**
     * Returns the ColumnValidator of the passed userRecord
     * @param {TSBcolumnOption} TSBcolumnOption - The options needs to be met inorder to be sent to TSB db
     * @param {String[]} userColumns
     * @param {Object} userRecord
     * @returns {ColumnValidator}
     */
    validate_and_construct = (TSBcolumnOption, userColumns, userRecord) => {
        // find and merge userColumns data in userRecord
        // 1- Merge userColumns data in userRecord as validatedData
        // 2- validate that validatedData is meeting the TSBcolumnOption
        // 3- return ColumnValidator Object with its attributes

        /** @type {boolean} */
        let isValid = true;

        /** @type {(string|null)} */
        let message = null;

        /** @type {(string|number|null)} */
        let validatedData;


        if (TSBcolumnOption.column === "Currency")
            validatedData = userColumns.join('');
        else
            validatedData = userColumns.map(userColumn => userRecord[userColumn]).filter(item => item).join(' ').trim();


        if (TSBcolumnOption.type.includes("VARCHAR")) {
            // get number from varchar then validate string length
            const string_length = /\(([^)]+)\)/.exec(TSBcolumnOption.type)[1];

            if (validatedData) {
                if (validatedData.length > string_length) {
                    isValid = false;
                    message = `${validatedData} is exceeding the string length ${string_length}`
                }
            } else if (!validatedData && !TSBcolumnOption.nullable) {
                isValid = false;
                message = `${userColumns} can't be null in ${JSON.stringify(userRecord)}`
            }
        }

        if (TSBcolumnOption.type === "FLOAT") {
            if (validatedData) {
                validatedData = Number(validatedData);
                if (isNaN(validatedData)) {
                    isValid = false;
                    message = `${validatedData} Should be Numbers only`
                } else if (!validatedData && !TSBcolumnOption.nullable) {
                    isValid = false;
                    message = `${userColumns} can't be null in ${JSON.stringify(userRecord)}`
                }
            }
        }

        return {
            data: validatedData,
            message: message,
            isValid: isValid
        }
    };

    validate = () => {
        const {form: {validateFields}, excelFile, databaseOptions, databaseType} = this.props;

        validateFields((errors, columns) => {
            // convert object to array of {ourColumn, excelColumn} pairs
            columns = Object.keys(columns).map(key => {
                return {ourColumn: key, excelColumn: columns[key]};
            });

            /** @type {SelectedColumn[]} */
            const selectedColumns = columns.filter(column => !!column.excelColumn).filter(column => !!column.excelColumn[0]);

            /** @type {NewRecord[]} */
            let validRecords = [];

            /** @type {NewRecord[]} */
            let invalidRecords = [];

            for (const user_record of excelFile.data) {
                /** @type {NewRecord} */
                let record = {};

                for (const selectedColumn of selectedColumns) {
                    const {ourColumn, excelColumn} = selectedColumn;

                    /** @type {TSBcolumnOption} */
                    const TSBcolumnOption = databaseOptions[databaseType].find(databaseOptions => databaseOptions.column === ourColumn);

                    /** @type {ColumnValidator} */
                    record[ourColumn] = this.validate_and_construct(TSBcolumnOption, [...excelColumn], user_record)
                }

                if (Object.values(record).flatMap(value => value.isValid).indexOf(false) > -1)
                    invalidRecords.push(record);
                else
                    validRecords.push(record);
            }

            console.log(validRecords, invalidRecords);

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

