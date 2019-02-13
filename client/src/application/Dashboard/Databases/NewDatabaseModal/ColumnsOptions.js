import React from 'react'

export const ColumnsOptions = (columnHeader, type) => {
    return Object.keys(columnHeader).map((c, index) => {
        if (type === "db") {
            if (c === "ID")
                return {
                    title: c,
                    dataIndex: c,
                    key: index,
                    width: 80,
                    fixed: 'left'
                };
            else
                return {
                    title: c,
                    dataIndex: c,
                    key: index,
                    width: 150
                };
        } else
            return {
                title: c,
                dataIndex: c,
                key: index,
                width: 100,
                render: item => <span>{
                    item.isValid ?
                        (
                            item.data.day ?
                                [item.data.year, item.data.month, item.data.day].join('/')
                                :
                                item.data
                        )
                        :
                        (
                            <p style={{backgroundColor: '#ff7875'}}> {item.message}</p>
                        )
                }</span>

            }
    });
};