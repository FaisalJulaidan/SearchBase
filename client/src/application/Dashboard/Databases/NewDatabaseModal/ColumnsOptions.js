import React from 'react'

export const ColumnsOptions = (columnHeader) =>
    Object.keys(columnHeader).map((c, index) => {
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
