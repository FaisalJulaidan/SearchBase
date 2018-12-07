import React, {Component} from 'react';

import "./Header.less"
import styles from "./Header.module.less";
import {Button} from "antd";
import PropTypes from 'prop-types';


class Header extends Component {
    static contextTypes = {
        router: PropTypes.object
    };

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
