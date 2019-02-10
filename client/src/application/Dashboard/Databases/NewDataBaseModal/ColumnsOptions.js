import React from 'react'

export const ColumnsOptions = (columns) => Object.keys(columns).map((c, index) => {
    if (c === "Name" || c === "Email")
        return {
            title: c,
            dataIndex: c,
            key: index,
            fixed: 'left',
        };
    else
        return {
            title: c,
            dataIndex: c,
            key: index,
        }
});
