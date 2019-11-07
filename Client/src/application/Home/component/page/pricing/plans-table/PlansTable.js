import React from 'react';
import styles from './plans-table.module.css'
import {Table} from "react-bootstrap";
import TableStructure from './plans-table-structure.json'
import PlansTableSection from "./PlansTableSection";

const PlansTable = (props) => {
    let tables = Object.keys(TableStructure).map((section, i) => {
        return (
            <PlansTableSection key={i} index={i} sectionKey={section}/>
        )
    });
    return (
        <Table hover className={`${styles.table} ${props?.className}`}>
            {tables}
        </Table>
    );
};

export default PlansTable;