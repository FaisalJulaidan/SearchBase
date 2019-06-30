import React from 'react';
import styles from "./AuroraSuccess.module.less"

class AuroraSuccess extends React.Component {
    render() {
        return (
            <div className={styles.SuccessCheckmark}>
                <div className={styles.CheckIcon}>
                    <span className={[styles.IconLine, styles.LineTip].join(' ')}/>
                    <span className={[styles.IconLine, styles.LineLong].join(' ')}/>
                    <div className={styles.IconCircle}/>
                    <div className={styles.IconFix}/>
                </div>
            </div>
        );
    }
}

export default AuroraSuccess
