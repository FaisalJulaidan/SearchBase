import React from "react";
import styles from './Thinking.module.css'

const Thinking = () => {
    return (
        <div className={styles.ParentDots}>
            <div className={styles.Dots}></div>
            <div className={styles.Dots}></div>
            <div className={styles.Dots}></div>
        </div>
    );
};

export default Thinking;
