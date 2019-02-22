import React, {Component} from 'react';

import styles from "./Header.module.less";
import {Button} from "antd";
import PropTypes from 'prop-types';


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
                                    <Button onClick={this.context.router.history.goBack}
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
