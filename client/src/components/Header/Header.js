import React, {Component} from 'react';

import styles from "./Header.module.less";
import {Button} from "antd";
import PropTypes from 'prop-types';


class Header extends Component {
    static contextTypes = {
        router: PropTypes.object
    };

    render() {

        return (
            <div style={{height: 56, marginBottom: 10}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div style={{display: '-webkit-inline-box'}}>
                            <Button onClick={this.context.router.history.goBack}
                                    type="primary" icon="left" shape="circle" size={"small"}></Button>
                            <h3>{this.props.assistantName || this.props.display}</h3>
                        </div>

                    </div>
                </div>
            </div>
        );
    }
}

export default Header;
