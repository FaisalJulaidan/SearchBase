import React, {Component} from 'react';
import styles from "./NoHeaderPanel.module.less";


class NoHeaderPanel extends Component {

    render() {
        return (
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Body}>
                        {this.props.children}
                    </div>
                </div>
            </div>
        );
    }
}

export default NoHeaderPanel;
