import React, {Component} from 'react';
import {Spin} from 'antd';
import styles from "./NoHeaderPanel.module.less";
import Spinner from 'components/LoadingSpinner/LoadingSpinner'

class NoHeaderPanel extends Component {

    constructor(props) {
        super(props);
    }

    TitleElementRef = {};
    BodyElementRef = {};

    render() {
        const TitleElement = React.Children.only(this.props.children[0]);
        const BodyElement = React.Children.only(this.props.children[1]);
        return (
            this.props.loading ?
                <Spin/>
                :
                <div style={{height: '100%'}}>
                    <div className={styles.Panel} styles={this.props.panelStyles}>
                        <div className={styles.Panel_Body}>
                            {React.cloneElement(TitleElement, {ref: el => this.TitleElementRef = el})}
                            {React.cloneElement(BodyElement, {ref: el => this.BodyElementRef = el})}
                        </div>
                    </div>
                </div>
        );
    }
}

export default NoHeaderPanel;
