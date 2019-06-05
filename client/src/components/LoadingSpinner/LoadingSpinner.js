import React from 'react';
import styles from "./LoadingSpinner.module.less"

class LoadingSpinner extends React.Component {
    render() {
        return (
            <div className={styles.Loader}>
                Loading...
            </div>
        );
    }
}
export default LoadingSpinner
