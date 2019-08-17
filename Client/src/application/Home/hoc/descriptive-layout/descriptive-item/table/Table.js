import React from 'react';
import styles from './table.module.css';
import {Table as ReactTable} from "react-bootstrap";
import PropTypes from "prop-types";
import TableRow from "./table-row/TableRow";

const Table = (props) => {

    let headRows = props.head.map((row, i) => {
        return <TableRow key={i} head row={row}/>
    });

    let bodyRows = props.body.map((row, i) => {
        return <TableRow key={i} body row={row}/>
    });

    return (
        <ReactTable className={styles.table} striped bordered hover>
            <thead>{headRows}</thead>
            <tbody>{bodyRows}</tbody>
        </ReactTable>
    );

};

Table.propTypes = {
    head: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.shape({
        text: PropTypes.string,
        items: PropTypes.arrayOf(PropTypes.string)
    }))),
    body: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.shape({
        text: PropTypes.string,
        items: PropTypes.arrayOf(PropTypes.string)
    })))
};

export default Table;
