import React from 'react';
import PropTypes from 'prop-types';
import {Col, Row} from 'antd';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import styles from './PublicNavbar.module.less'

const PublicNavbar = ({companyLogo}) => {

    return (
        <div>
            <Row>
                <Col span={8} xs={24} className={styles.Navbar}>
                    <div style={{display: 'flex'}}>
                        {
                            companyLogo ?
                                <img src={companyLogo} alt="company logo" height={40}/>
                                :
                                <>
                                    <FontAwesomeIcon size="2x" icon={faCloud} style={{color: '#9254de'}}/>
                                    <div style={{
                                        lineHeight: '40px',
                                        marginLeft: 18,
                                        color: "#9254de"
                                    }}>
                                        TheSearchBase
                                    </div>
                                </>
                        }

                    </div>
                </Col>
            </Row>
        </div>
    );

};

PublicNavbar.propTypes = {
    companyLogo: PropTypes.string,
};

export default PublicNavbar;
