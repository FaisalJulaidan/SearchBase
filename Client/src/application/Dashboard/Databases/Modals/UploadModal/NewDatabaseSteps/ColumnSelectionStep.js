import { Form, message, Select, Spin } from 'antd';

import React, { Component } from 'react';
import './UploadDatabaseStep/UploadDatabaseStep.less';

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
 @property {(string|number|null|Date)} data - the record's data.
 @property {(string|null)} message - if not valid here will be a message.
 @property {boolean} isValid - to check if valid or not.
 @property {string[]} originalColumns - the columns in the uploaded file.
 */

/**
 * The constructed record before check if valid or not
 @typedef NewRecord
 @type {Object.<string, ColumnValidator>}
 */

/**
 * Date type
 @typedef Date
 @type {Object}
 @property {string} year
 @property {string} month
 @property {string} day
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

        /** @type {(string|number|null|Date)} */
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

        if (TSBcolumnOption.type === "FLOAT" || TSBcolumnOption.type === "INTEGER") {
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

        if (TSBcolumnOption.type === "DATETIME") {
            const date = new Date(validatedData);

            validatedData = {
                year: date.getUTCFullYear(),
                month: date.getMonth() + 1,
                day: date.getDate()
            };

            if (!validatedData.year || !validatedData.month || !validatedData.day) {
                isValid = false;
                message = `${JSON.stringify(validatedData)} You should pass dates only`
            }
        }


        if (TSBcolumnOption.column === 'CandidateMobile') {
            // if there is +44, then do nothing
            // if there is (.*) remove it then check if there is +44
            // if there is 44 only remove it

            if (
                userColumns.length > 1 // there is country code
            ) {

                validatedData = validatedData.split(' ').join('').replace(/\(.*\)/, '').replace('-', '');
                if (!validatedData.includes(userColumns[0])) {

                    if (!validatedData.includes(userColumns[0].replace('+', '')))
                        validatedData = userColumns[0] + validatedData;

                    if (!validatedData.includes('+'))
                        validatedData = '+' + validatedData;

                    if (!validatedData.includes(userColumns[0]))
                        validatedData = userColumns[0] + validatedData;


                }

            }





        }

        return {
            data: validatedData,
            message: message,
            isValid: isValid,
            originalColumns: userColumns
        }
    };

    /**
     * @returns {Promise} Promise object represents the valid and invalid data
     */
    parseForm = () => new Promise((resolve, reject) => {
        const {form: {validateFields}, excelFile, databaseOptions, databaseType} = this.props;
        validateFields((errors, columns) => {
            if (errors) {
                message.error('Select a value for the required fields');
                return reject('Rejected');
            }

            if (!excelFile.data) {
                message.error('Please check your CSV file try to add more than one single record');
                return reject('Rejected');
            }

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

            if (selectedColumns[0])
                return resolve({
                    validRecords: validRecords,
                    invalidRecords: invalidRecords
                });
            else {
                message.error('Select at least one column');
                return reject('Rejected');
            }
        });
    });

    //s
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
                {!!databaseOptions ?
                    <Form layout='horizontal'>
                        {databaseOptions[databaseType].map((type, index) => {
                            if (type.column === "Currency") return (
                                <FormItem label={type.column} {...formItemLayout} key={index}>
                                    {getFieldDecorator(type.column, {
                                        defaultValue: selectedColumns,
                                        rules: [{required: !type.nullable, message: 'This is required field',}]
                                    })
                                    (
                                        <Select key={index} placeholder="Please select currency">
                                            {databaseOptions.currencyCodes.map(
                                                (currencyCode, index) =>
                                                    <Option key={index} value={currencyCode}>{currencyCode}</Option>
                                            )}
                                        </Select>
                                    )}
                                </FormItem>
                            );

                            else return (
                                <FormItem label={type.column} {...formItemLayout} key={index}>
                                    {getFieldDecorator(type.column, {
                                        defaultValue: selectedColumns,
                                        rules: [{required: !type.nullable, message: 'This is required field',}]
                                    })
                                    (
                                        <Select mode="multiple" mode="tags" placeholder="Select Column or Columns"
                                                onDeselect={this.handleRemove}
                                                onChange={this.handleChange}>
                                            {filteredOptions.map(item => (
                                                <Select.Option key={item} value={item}>{item}</Select.Option>
                                            ))}
                                        </Select>
                                    )}
                                </FormItem>
                            );
                        })}
                    </Form>
                    : <Spin/>}

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

