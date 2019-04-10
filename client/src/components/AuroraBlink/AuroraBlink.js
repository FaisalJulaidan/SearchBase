import React from 'react';
import styles from "./AuroraBlink.module.less"
import PropTypes from 'prop-types';


const AuroraBlink = ({color}) => (
    <svg className={styles.Pulse} x="0px" y="0px" viewBox="0 0 100 100">
        <circle className={styles.PulseDisk} cx="50" cy="50" fill={color}/>
        <circle className={styles.PulseCircle} cx="50" cy="50" strokeWidth="2" stroke={color}/>
        <circle className={styles.PulseCircle2} cx="50" cy="50" strokeWidth="2" stroke={color}/>
    </svg>
);


AuroraBlink.propTypes = {
    color: PropTypes.string.isRequired,
};
export default AuroraBlink
