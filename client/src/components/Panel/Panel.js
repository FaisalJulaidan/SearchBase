import React from 'react';

import "./Header.less"
import styles from "./Panel.module.less";
import PropTypes from 'prop-types';


// Not complete yet...
const Panel = (props) => {
    return (
        <div className={styles.Panel}>
            <div className={styles.Panel_Header}>


            </div>
            <div className={styles.Panel_Body}>

            </div>
        </div>
    );

};

Panel.propTypes = {
    assistantName: PropTypes.string,
};

export default Panel;
