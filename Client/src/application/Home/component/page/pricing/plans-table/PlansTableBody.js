import React from 'react';
import styles from './plans-table-body.module.css';
import PropTypes from 'prop-types';
import TableStructure from './plans-table-structure.json'
import TableData from './plans-table-data.json'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck} from "@fortawesome/free-solid-svg-icons";

const PlansTableBody = props => {
    let getPlansData = (item) => {
        return Object.keys(TableData).map((plan, i) => {
            if (TableData[plan][item] === true)
                return <td key={i} className={styles.td_plan}><FontAwesomeIcon color="#4CAF50" size="2x" icon={faCheck}/></td>;
            else
                return <td key={i} className={styles.td_plan}>{TableData[plan][item]}</td>;
        });
    };

    let rows = TableStructure[props.sectionKey].map((key, i) => {
        return (
            <tr key={i}>
                <td className={styles.td}>{key}</td>
                {getPlansData(key)}
            </tr>
        );
    });

    return (
        <tbody>
        {rows}
        </tbody>
    );
};

PlansTableBody.propTypes = {
    sectionKey: PropTypes.string.isRequired,
};

export default PlansTableBody;