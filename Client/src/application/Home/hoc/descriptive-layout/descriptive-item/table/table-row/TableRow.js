import React from 'react';
import PropTypes from "prop-types";
import TableItem from "../table-item/TableItem";

const TableRow = (props) => {

    let columns = props.row.map((column, i) => {
        return <TableItem key={i} head={props.head} body={props.body} column={column}/>
    });

    return (
        <tr>
            {columns}
        </tr>
    );
};

TableRow.prototypes = {
    head: PropTypes.bool,
    body: PropTypes.bool,
    row: PropTypes.arrayOf(PropTypes.shape({
        text: PropTypes.string,
        items: PropTypes.arrayOf(PropTypes.string)
    }))
};

export default TableRow;
