import React from 'react';
// Styles
// import styles from './styles/Header.module.css';
import './styles/Header.css';
// Components
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloud } from '@fortawesome/free-solid-svg-icons';
import { Button, Col, Row, Tooltip } from 'antd';

const Header = ({ title, logoPath, isDirectLink, resetChatbot, closeWindow }) => {
    return (
        <div className={'Header'}>
            <Row>
                {
                    !isDirectLink ?
                        <Col span={3}>
                            {
                                logoPath ?
                                    <img alt="header" width={30}
                                         src={`${process.env.REACT_APP_ASSETS_PUBLIC_URL}${process.env.NODE_ENV}/company_logos/${logoPath}`}/> :
                                    <FontAwesomeIcon size="2x" icon={faCloud} style={{ color: '#673AB7' }}/>
                            }
                        </Col>
                        : <Col span={3}/>
                }

                <Col span={16}>
                    <div className={'H3'}>{title}</div>
                </Col>
                <Col span={5} style={{ textAlign: 'right', position: 'relative' }}>
                    <Tooltip title="Reset"
                             getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}>
                        <Button className={'Button'} onClick={resetChatbot}
                                type="default" shape="circle" icon="redo" size={'small'}/>
                    </Tooltip>
                    {
                        isDirectLink ? '' :
                            <Tooltip title="Close"
                                     getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}>
                                <Button className={['Button', 'Danger'].join(' ')}
                                        onClick={closeWindow}
                                        type="danger" shape="circle" icon="close"
                                        style={{ display: isDirectLink ? 'none' : '' }}
                                        size={'small'}/>
                            </Tooltip>
                    }


                </Col>
            </Row>
        </div>
    );
};

export default Header;