import React, { useEffect, useState } from 'react';
// Styles
// import styles from './styles/Header.module.css';
import './styles/Header.css';
// Components
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloud } from '@fortawesome/free-solid-svg-icons';
import { Button, Col, Row, Tooltip } from 'antd';

const Header = ({ title, logoPath, isDirectLink, resetChatbot, closeWindow }) => {

    const privacyPolicy = () => {
        let win = window.open('https://www.thesearchbase.com/privacy', '_blank');
        win.focus();
    };

    const isMobile = useWindowSize().width <= 420;

    // Hook
    function useWindowSize() {
        const isClient = typeof window === 'object';

        function getSize() {
            return {
                width: isClient ? window.innerWidth : undefined,
                height: isClient ? window.innerHeight : undefined
            };
        }

        const [windowSize, setWindowSize] = useState(getSize);

        useEffect(() => {
            if (!isClient) {
                return false;
            }

            function handleResize() {
                setWindowSize(getSize());
            }

            window.addEventListener('resize', handleResize);
            return () => window.removeEventListener('resize', handleResize);
        }, []); // Empty array ensures that effect is only run on mount and unmount

        return windowSize;
    }

    return (
        <div className={'Header'} id={'Chatbot_Header'}>
            <Row style={{ width: '100%' }}>
                {
                    !isDirectLink &&
                    <Col span={3}>
                        {
                            logoPath ?
                                <img alt="header" width={30}
                                     src={`${logoPath}?timestamp=${new Date().getTime()}`}/> :
                                <FontAwesomeIcon size="2x" icon={faCloud} style={{ color: '#673AB7' }}/>
                        }
                    </Col>
                }

                {
                    isDirectLink && isMobile &&
                    <Col span={3}>
                        {
                            logoPath ?
                                <img alt="header" width={30}
                                     src={`${logoPath}?timestamp=${new Date().getTime()}`}/> :
                                <FontAwesomeIcon size="2x" icon={faCloud} style={{ color: '#673AB7' }}/>
                        }
                    </Col>
                }

                <Col span={!isDirectLink || isDirectLink && isMobile ? 14 : 17}>
                    <div className={'H3'}>{title}</div>
                </Col>

                <Col span={7} style={{ textAlign: 'right', position: 'relative' }}>
                    <Tooltip title="View our privacy policy"
                             getPopupContainer={() => document.getElementById('TheSearchBase_Chatbot')}>
                        <Button className={'Button'} onClick={privacyPolicy}
                                type="default" shape="circle" icon="lock" size={'small'}/>
                    </Tooltip>

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
                                        shape="circle" icon="close"
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
