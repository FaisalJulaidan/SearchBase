import React from "react";
import styles from "./UsersDisplay.less";

import {
    Table, Input, InputNumber, Popconfirm, Form,
} from 'antd';
import {isEmpty} from "lodash";


const data = [];
const FormItem = Form.Item;
const EditableContext = React.createContext();

const EditableRow = ({ form, index, ...props }) => (
    <EditableContext.Provider value={form}>
        <tr {...props} />
    </EditableContext.Provider>
);

const EditableFormRow = Form.create()(EditableRow);

class EditableCell extends React.Component {
    getInput = () => {
        if (this.props.inputType === 'number') {
            return <InputNumber />;
        }
        return <Input />;
    };

    render() {
        const {
            editing,
            dataIndex,
            title,
            inputType,
            record,
            index,
            ...restProps
        } = this.props;
        return (
            <EditableContext.Consumer>
                {(form) => {
                    const { getFieldDecorator } = form;
                    return (
                        <td {...restProps}>
                            {editing ? (
                                <FormItem style={{ margin: 0 }}>
                                    {getFieldDecorator(dataIndex, {
                                        rules: [{
                                            required: true,
                                            message: `Please Input ${title}!`,
                                        }],
                                        initialValue: record[dataIndex],
                                    })(this.getInput())}
                                </FormItem>
                            ) : restProps.children}
                        </td>
                    );
                }}
            </EditableContext.Consumer>
        );
    }
}

class UsersDisplay extends React.Component {
    constructor(props) {
        super(props);
        this.state = { data, editingKey: '' };
        this.columns = [
            {
                title: 'Name',
                dataIndex: 'Fullname',
                width: '31%',
                editable: true,
            },
            {
                title: 'Email',
                dataIndex: 'Email',
                width: '35%',
                editable: true,
            },
            {
                title: 'Role',
                dataIndex: 'RoleName',
                width: '18%',
                editable: true,
            },
            {
                title: 'Action',
                dataIndex: 'operation',
                render: (text, record) => {
                    const editable = this.isEditing(record);
                    return (
                        <div>
                            {editable ? (
                                <span>
                  <EditableContext.Consumer>
                    {form => (
                        <a
                            href="javascript:;"
                            onClick={() => this.save(form, record.key)}
                            style={{ marginRight: 8 }}
                        >
                            Save
                        </a>
                    )}
                  </EditableContext.Consumer>
                  <Popconfirm
                      title="Sure to cancel?"
                      onConfirm={() => this.cancel(record.key)}
                  >
                    <a>Cancel</a>
                  </Popconfirm>
                </span>
                            ) : (
                                <a onClick={() => this.edit(record.key)}>Edit</a>
                            )}
                        </div>
                    );
                },
            },
        ];
    }

    componentWillReceiveProps(nextProps){
        let data = nextProps.users;
        if(!isEmpty(data)){
            if(data !== this.state.data){
                data = data.map((record, index) => {data[index]["key"] = data[index]["ID"]; return record});

                data = data.map((record, index) => {
                    data[index]["Fullname"] = data[index]["Firstname"] + " " + data[index]["Surname"];
                    return record
                });

                data = data.map((record, index) => {data[index]["RoleName"] = data[index]["Role"]["Name"]; return record});

                this.setState({
                    data: data
                });
            }
        }
    }

    isEditing = record => record.key === this.state.editingKey;

    cancel = () => {
        this.setState({ editingKey: '' });
    };

    save(form, key) {
        form.validateFields((error, row) => {
            if (error) {
                return;
            }
            const newData = [...this.state.data];
            const index = newData.findIndex(item => key === item.key);
            if (index > -1) {
                const item = newData[index];
                newData.splice(index, 1, {
                    ...item,
                    ...row,
                });
                this.setState({ data: newData, editingKey: '' });
            } else {
                newData.push(row);
                this.setState({ data: newData, editingKey: '' });
            }
        });
    }

    edit(key) {
        this.setState({ editingKey: key });
    }

    render() {
        const components = {
            body: {
                row: EditableFormRow,
                cell: EditableCell,
            },
        };
        console.log("STATE", this.state)
        const columns = this.columns.map((col) => {
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

export default UsersDisplay;