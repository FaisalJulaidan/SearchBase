import React from 'react';
import styles from './plans-table-head.module.css'
import PropTypes from 'prop-types';
import TableData from './plans-table-data.json'

const PlansTableHead = props => {

    let plans = <th/>;
    if (props.index === 0) {
        plans = Object.keys(TableData).map((key, i) => {
            return <th key={i} className={styles.th_plan}>{key}</th>
        });
    }
    return (
        <thead className={styles.thead}>
        <tr>
            <th colSpan={props.index === 0 ? 1 : 4} className={styles.th}>{props.sectionKey}</th>
            {props.index === 0 && plans}
        </tr>
        </thead>
    );
};

PlansTableHead.propTypes = {
    sectionKey: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired
};

export default PlansTableHead;