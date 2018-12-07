import React, {Component} from 'react';

import "./Header.less"
import styles from "./Header.module.less";
import {Button} from "antd";


class Header extends Component {
    static contextTypes = {
        router: () => true, // replace with PropTypes.object if you use them
    }

    render() {
        return (
            <div className={styles.Panel}>
                <div className={styles.Header}>
                    <div style={{display: '-webkit-inline-box'}}>
                        <Button onClick={this.context.router.history.goBack}
                                type="primary" icon="left" shape="circle" size={"small"}></Button>
                        <h3>{this.props.assistantName}</h3>
                    </div>

                </div>
            </div>
        );
    }
}

export default Header;
