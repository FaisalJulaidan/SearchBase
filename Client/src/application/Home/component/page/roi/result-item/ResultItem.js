import React from 'react';
import styles from './result-item.module.css'
import PropTypes from 'prop-types';

const ResultItem = props => {

    let valSize = '2.5em';
    let valFontWeight = 'normal';
    switch (props.valSize) {
        case 'small':
            valSize = '1.5em';
            valFontWeight = 'lighter';
            break;
        case 'big':
            valSize = '4em';
            valFontWeight = 'bold';
            break;
        case 'large':
            valSize = '6em';
            valFontWeight = 'bold';
            break;
    }

    return (
        <div>
            <h2 className={styles.value} style={{fontSize: valSize, fontWeight: valFontWeight}}>{props.currency?'£':''}{props.value}</h2>
            <h1 className={styles.title}>{props.title}</h1>
        </div>
    );
};

ResultItem.propTypes = {
    value: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    currency: PropTypes.bool,
    valSize: PropTypes.oneOf(["small", "big", "large"])
};

export default ResultItem;