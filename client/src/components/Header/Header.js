import React, {Component} from 'react';

import styles from "./Header.module.less";
import {Button} from "antd";
import PropTypes from 'prop-types';
import {history} from "helpers";


class Header extends Component {
    static contextTypes = {
        router: PropTypes.object
    };

    render() {
        let showBackButton = true;
        let button = this.props.button;
        if (this.props.showBackButton === false)
            showBackButton = false;


        return (
            <div style={{height: 56, marginBottom: 10}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>

                        <div style={{display: '-webkit-inline-box'}}>
                            {
                                showBackButton ?
                                    <Button onClick={history.goBack}
                                            type="primary" icon="left" shape="circle"
                                            size={"small"}/>
                                    : null
                            }
                            <h3>{this.props.assistantName || this.props.display}</h3>
                        </div>
                        <div>
                            {
                                button ?
                                    <Button className={styles.Panel_Header_Button}
                                            type="primary"
                                            icon={this.props.button.icon}
                                            disabled={this.props.button.disabled}
                                            loading={this.props.button.loading}
                                            onClick={this.props.button.onClick}>
                                        {this.props.button.text}
                                    </Button>
                                    : null
                            }
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Header;
