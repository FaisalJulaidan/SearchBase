import React from "react";
import styles from "./UsersDisplay.less";

import {Form, Table,} from 'antd';
import EditableFormRow from "./EditableRow/EditableRow";
import EditableCell from "./EditableCell/EditableCell";
import Columns from "./Columns/Columns"


class UsersDisplay extends React.Component {

    isEditing = record => {
        return record.key === this.state.editingKey;
    };

    cancel = () => {
        this.setState({editingKey: ''});
    };

    save = (form, key) => {
        this.props.form.validateFields((error, row) => {
            if (error) {
                return;
            }
            console.log("this.state.data", this.state.data)
            console.log("key", key)
            console.log("form", form)
            console.log("row", row)
            const newData = [...this.state.data];
            const index = newData.findIndex(item => key === item.key);
            console.log("index", index)
            if (index > -1) {
                const item = newData[index];
                newData.splice(index, 1, {
                    ...item,
                    ...row,
                });
                console.log("newData", newData)
                this.setState({data: newData, editingKey: ''});
            } else {
                newData.push(row);
                this.setState({data: newData, editingKey: ''});
            }
        });
    };

    edit = key => {
        this.setState({editingKey: key});
    };

    state = {
        data: [{key: "test", name:"tester", age: 32, address:"test road"}],
        editingKey: "",
        columns: Columns(this.isEditing, this.save, this.cancel, this.edit, this.props.form)
    };

    render() {
        const components = {
            body: {
                row: EditableFormRow,
                cell: EditableCell,
            },
        };

        const columns = this.state.columns.map((col) => {
            if (!col.editable) {
                return col;
            }
            return {
                ...col,
                onCell: record => ({
                    record,
                    inputType: col.dataIndex === 'age' ? 'number' : 'text',
                    dataIndex: col.dataIndex,
                    title: col.title,
                    editing: this.isEditing(record),
                }),
            };
        });

        return (
            <Table
                components={components}
                bordered
                dataSource={this.state.data}
                columns={columns}
                rowClassName="editable-row"
            />
        );
    }
}

export default Form.create()(UsersDisplay);