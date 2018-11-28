import React, {Component} from 'react';

import "./Header.less"
import styles from "../Flow.module.less";


class Header extends Component {


    render() {
        return (
            <div className={styles.Panel}>
                <div className={styles.Header}>
                    <div>
                        <h3>Assistant Name</h3>
                    </div>
                </div>
            </div>
        );
    }
}

export default Header;
