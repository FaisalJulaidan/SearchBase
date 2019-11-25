import React from 'react';
import styles from './result-item.module.css'
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMinus} from "@fortawesome/free-solid-svg-icons";

const ResultItem = props => {

    let styleClassValue = styles.value;
    let styleClassTitle = styles.title;
    switch (props.valSize) {
        case 'small':
            styleClassValue = styles.value_small;
            styleClassTitle = styles.title_small;
            break;
        case 'large':
            styleClassValue = styles.value_big;
            styleClassTitle = styles.title_big;
            break;
    }

    let formatted = new Intl.NumberFormat('en-gb').format(props.value);
    return (
        <div className={styles.wrapper}>
            <span className={`${styles.value} ${styleClassValue}`}>
                {(props.currency ? `£${formatted}` : `${formatted}`)}
            </span>
            <h1 className={`${styles.title} ${styleClassTitle}`}>{props.title}</h1>
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