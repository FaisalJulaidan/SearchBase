import React from 'react';
import styles from './result-item.module.css'
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMinus} from "@fortawesome/free-solid-svg-icons";

const ResultItem = props => {

    let valSize = '2.5em';
    let titleSize = '0.85em';
    let valFontWeight = 'normal';
    let fontAwesomeSize = '2x';
    let iconMargin = '.25em 0';
    switch (props.valSize) {
        case 'small':
            valSize = '1.5em';
            valFontWeight = 'lighter';
            fontAwesomeSize = "1x";
            titleSize = '0.75em';
            iconMargin = '0';
            break;
        case 'large':
            valSize = '6em';
            valFontWeight = 'bold';
            fontAwesomeSize = "3x";
            titleSize = '1em';
            iconMargin = '.5em 0';
            break;
    }

    let isZero = () => {
        if (Number.isInteger(props.value))
            return props.value === 0;
        else
            return props.value === "0";
    };

    return (
        <div className={styles.wrapper}>
            <div className={styles.value_wrapper}>
            <span className={styles.value} style={isZero() ? {} : {fontSize: valSize, fontWeight: valFontWeight}}>
                {isZero()
                    ? <FontAwesomeIcon size={fontAwesomeSize} style={{margin: iconMargin}} className={styles.icon}
                                       icon={faMinus}/>
                    : (props.currency ? `£${props.value}` : `${props.value}`)
                }
            </span>
            </div>
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