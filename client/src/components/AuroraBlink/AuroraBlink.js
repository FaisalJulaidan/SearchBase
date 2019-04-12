import React from 'react';
import styles from "./AuroraBlink.module.less"
import PropTypes from 'prop-types';


const AuroraBlink = ({color, style}) => (
    <svg className={styles.Pulse}
         style={style}
         x="0px" y="0px" viewBox="0 -21 1 40">
        <circle className={styles.PulseDisk} cx="0" cy="0" fill={color}/>
        <circle className={styles.PulseCircle} cx="0" cy="0" strokeWidth="2" stroke={color}/>
        <circle className={styles.PulseCircle2} cx="0" cy="0" strokeWidth="2" stroke={color}/>
    </svg>
);


AuroraBlink.propTypes = {
    color: PropTypes.string.isRequired,
    style: PropTypes.object.isRequired,
};
export default AuroraBlink
