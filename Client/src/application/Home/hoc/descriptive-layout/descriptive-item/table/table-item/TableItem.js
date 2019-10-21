import React from 'react';
import styles from './table-item.module.css';
import PropTypes from "prop-types";

const TableItem = (props) => {

    let item;
    if ((typeof props.column.text != "undefined")) {
        item = props.column.text;
    } else if ((typeof props.column.items != "undefined")) {
        let listItems = props.column.items.map((item, i) => {
            return <li className={styles.li} key={i}>{item}</li>
        });
        item = <ol>{listItems}</ol>
    } else {
        item = <></>;
    }

    if (props.head)
        return (
            <th className={styles.head}>{item}</th>
        );
    else if (props.body)
        return (
            <td className={styles.body}>{item}</td>
        );
    else
        return (
            <td className={styles.body}>{item}</td>
        );
};

TableItem.prototypes = {
    head: PropTypes.bool,
    body: PropTypes.bool,
    column: PropTypes.shape({
        text: PropTypes.string,
        items: PropTypes.arrayOf(PropTypes.string)
    })
};

export default TableItem;
