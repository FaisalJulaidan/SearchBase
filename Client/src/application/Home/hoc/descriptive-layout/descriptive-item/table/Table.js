import React from 'react';
import styles from './table.module.css';
import {Table as ReactTable} from "react-bootstrap";
import PropTypes from "prop-types";
import TableRow from "./table-row/TableRow";
import {BREAKPOINTS} from "../../../../../../constants/config";

const Table = (props) => {

    let headRows = props.head.map((row, i) => {
        return <TableRow key={i} head row={row}/>
    });

    let bodyRows = props.body.map((row, i) => {
        return <TableRow key={i} body row={row}/>
    });

    let sizeProp = {};
    if (window.innerWidth < BREAKPOINTS.sm) {
        sizeProp["size"] = "sm";
        sizeProp["responsive"] = "sm";
    }

    return (
        <ReactTable className={styles.table} striped bordered hover {...sizeProp}>
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
