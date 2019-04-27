import React from 'react';
import PropTypes from 'prop-types';
import styles from "./CreateNewBox.module.less"

const CreateNewBox = (props) => {
    return (
        <div className={styles.Box}>
            <div className={styles.Icon}>
                <div className={styles.Plus}>+</div>
            </div>
            <div className={styles.Text}> Create assistant</div>
        </div>
    );

};


CreateNewBox.propTypes = {

};

export default CreateNewBox