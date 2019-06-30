import React from 'react'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import {Button as AntdButton, Col, Row, Tooltip} from 'antd';

import 'antd/lib/col/style';
import 'antd/lib/row/style';
import 'antd/lib/tooltip/style';

import styles from './Header.module.css'

class Header extends React.Component {


    render() {
        const {assistant} = this.props;
        return (
            <div className={styles.Header}>
                <Row>
                    <Col span={3}>
                        {
                            assistant && assistant.LogoName ?
                                <img alt="header" width={30}
                                     src={`${process.env.REACT_APP_ASSETS_PUBLIC_URL}${process.env.NODE_ENV}/company_logos/${assistant.LogoName}`}/> :
                                <FontAwesomeIcon size="2x" icon={faCloud} style={{color: '#673AB7'}}/>
                        }
                    </Col>
                    <Col span={16}>
                        <div className={styles.H3}>{this.props.topBarText}</div>
                    </Col>
                    <Col span={5} style={{textAlign: 'right'}}>
                        <Tooltip title="Reset" getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}>
                            <AntdButton className={styles.AntdButton}
                                        onClick={this.props.reseted}
                                        type="default" shape="circle" icon="redo"
                                        size={"small"}/>
                        </Tooltip>
                        <Tooltip title="Close" getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}>
                            <AntdButton className={[styles.AntdButton, styles.Danger].join(' ')}
                                        onClick={this.props.closed}
                                        type="danger" shape="circle" icon="close"
                                        style={{display: this.props.isDirectLink ? 'none' : ''}}
                                        size={"small"}/>
                        </Tooltip>

                    </Col>
                </Row>
            </div>
        );
    }
}

export default Header
