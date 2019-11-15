import React from 'react';
import styles from './result-item.module.css'
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMinus} from "@fortawesome/free-solid-svg-icons";

const ResultItem = props => {

    let valSize = '2.5em';
    let titleSize = '0.85em';
    let fontAwesomeSize = '2x';
    switch (props.valSize) {
        case 'small':
            valSize = '1.5em';
            fontAwesomeSize = "1x";
            titleSize = '0.75em';
            break;
        case 'large':
            valSize = '6em';
            fontAwesomeSize = "3x";
            titleSize = '.9em';
            break;
    }

    let formatted = new Intl.NumberFormat('en-gb').format(props.value);
    return (
        <div className={styles.wrapper}>
            <span className={styles.value} style={{fontSize: valSize}}>
                {(props.currency ? `£${formatted}` : `${formatted}`)}
            </span>
            <h1 className={styles.title} style={{fontSize: titleSize}}>{props.title}</h1>
        </div>
    );
};

ResultItem.propTypes = {
    value: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    currency: PropTypes.bool,
    valSize: PropTypes.oneOf(["small", "default", "large"])
};

export default ResultItem;