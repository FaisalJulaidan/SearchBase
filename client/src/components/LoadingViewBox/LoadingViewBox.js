import React from 'react';

import {Skeleton} from 'antd';
import styles from "components/LoadingViewBox/LoadingViewBox.module.less";

const LoadingViewBox = (props) => {
    return (
        <div className={styles.Box}>
            <div className={styles.Body}>
                <Skeleton active title={{width: 120}} className={styles.Title}>
                </Skeleton>
            </div>
        </div>
    )
};

export default LoadingViewBox
