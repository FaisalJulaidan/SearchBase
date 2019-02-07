import React from "react";
import {Popconfirm} from "antd";

const EditableContext = React.createContext();

const Columns = (isEditing, save, cancel, edit) => (
    [
        {
            title: 'name',
            dataIndex: 'name',
            width: '25%',
            editable: true,
        },
        {
            title: 'age',
            dataIndex: 'age',
            width: '15%',
            editable: true,
        },
        {
            title: 'address',
            dataIndex: 'address',
            width: '40%',
            editable: true,
        },
        {
            title: 'operation',
            dataIndex: 'operation',
            render: (text, record) => {
                console.log(text, record)
                const editable = isEditing(record);
                return (
                    <div>
                        {editable ? (
                            <span>
                  <EditableContext.Consumer>
                    {form => (
                        <a
                            href="javascript:;"
                            onClick={() => save(form, record.key)}
                            style={{marginRight: 8}}
                        >
                            Save
                        </a>
                    )}
                  </EditableContext.Consumer>
                  <Popconfirm
                      title="Sure to cancel?"
                      onConfirm={() => cancel(record.key)}
                  >
                    <a>Cancel</a>
                  </Popconfirm>
                </span>
                        ) : (
                            <a onClick={() => edit(record.key)}>Edit</a>
                        )}
                    </div>
                );
            },
        },
    ]
);

export default Columns;