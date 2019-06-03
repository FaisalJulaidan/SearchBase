import React from 'react';
import styles from "./CreateNewBox.module.less"
import PropTypes from 'prop-types';

const CreateNewBox = (props) => {
    return (
        <div className={styles.Box} style={{
            width: props.width || 300
        }}
             onClick={() => props.onClick()}>
            <div className={styles.Icon}>
                <div className={styles.Plus}>+</div>
            </div>
            <div className={styles.Text}> {props.text}</div>
        </div>
    );

};


CreateNewBox.propTypes = {
    width: PropTypes.number,
    text: PropTypes.string.isRequired,
};

export default CreateNewBox
