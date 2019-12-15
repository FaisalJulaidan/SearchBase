import React from 'react';
import styles from './footer.module.css'
import {Container, Row, Col} from 'react-bootstrap';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import {faAngellist, faLinkedinIn} from '@fortawesome/free-brands-svg-icons'
import {Link} from "react-router-dom";
import EmailShare from "react-email-share-link";
import {CURRENT_YEAR} from '../../../../constants/config';
import {ReactComponent as Wave} from './wave.svg';
import PropTypes from "prop-types";

const Footer = (props) => {
    return (
        <div style={{background: props.background}} className={styles.wrapper}>
            <Wave style={{background: props.background}} className={styles.wave}/>
            <footer id={props.id} className={styles.footer}>
                <Container>
                    <Row className={styles.row}>
                        <Col xs="auto" sm={4} md={6} lg={{span: 6, offset: 1}}
                             xl={{span: 7, offset: 1}}>
                            <div>
                                <Link className={styles.logo} to="/">
                                    <FontAwesomeIcon size="2x" icon={faCloud}/>
                                    <h1>SearchBase</h1>
                                </Link>
                            </div>
                            <p className={styles.address}>
                                Floor 6, Aldgate Tower
                                <br/>
                                London, E1 8FA
                                <br/>
                                (+44) 203-488-0918
                            </p>
                        </Col>
                        <Col xs="auto" className={styles.nav}>
                            <ul>
                                <li>Product</li>
                                <li><Link to={"/how-it-works#chatbot"}>Chatbots</Link></li>
                                <li><Link to={"/how-it-works#sms"}>SMS</Link></li>
                                <li><Link to={"/how-it-works"}>How it works?</Link></li>
                                {/* <li><Link to={"/release-notes"}>Release Note</Link></li> */}
                            </ul>
                        </Col>
                        <Col xs="auto" className={styles.nav}>
                            <ul>
                                <li>Company</li>
                                <li><Link to={"/our-team"}>Our team</Link></li>
                            </ul>
                        </Col>
                        <Col xs="auto" className={styles.nav}>
                            <ul>
                                <li>Support</li>
                                <li>
                                    <EmailShare email="info@SearchBase.com"
                                                subject="Contact"
                                                body="Hi, I would like to talk about...">
                                        {link => (<a href={link} data-rel="external">Contact us</a>)}
                                    </EmailShare>
                                </li>
                                <li>
                                    <EmailShare email="info@SearchBase.com"
                                                subject="Report a bug"
                                                body="Hi, I would like to report a bug in...">
                                        {link => (<a href={link} data-rel="external">Report a bug</a>)}
                                    </EmailShare>
                                </li>
                            </ul>
                        </Col>
                    </Row>
                    <Row className={styles.row}>
                        <Col className={styles.navigation_bottom} sm={12} md={9} lg={{span: 6, offset: 3}}
                             xl={{span: 6, offset: 3}}>
                            <ul>
                                <li><Link to={"/terms"}>Terms & Conditions</Link></li>
                                <li><Link to={"/privacy"}>Privacy Policy</Link></li>
                                <li><Link to={"/gdpr"}>GDPR</Link></li>
                            </ul>
                        </Col>
                        <Col className={styles.social_icons} sm={12} xs="auto" md={3} lg={{span: 3, offset: 0}}
                             xl={{span: 'auto', offset: 1}}>
                            <a target="_blank" rel="noopener noreferrer"
                               href="https://www.linkedin.com/company/thesearchbase">
                                <FontAwesomeIcon className={styles.icon} icon={faLinkedinIn}/>
                            </a>

                            <a target="_blank" rel="noopener noreferrer" href="https://angel.co/company/thesearchbase">
                                <FontAwesomeIcon className={styles.icon} icon={faAngellist}/>
                            </a>
                        </Col>
                    </Row>
                    <Row className={styles.row}>
                        <Col className={styles.copyright}>
                            <h4>Copyright SearchBase Ltd. {CURRENT_YEAR}. All rights reserved.</h4>
                            <h4> SearchBase Limited is registered and incorporated in England and Wales,company
                                registration number 11791408.</h4>
                        </Col>
                    </Row>
                </Container>
            </footer>
        </div>
    );
};

Footer.propTypes = {
    background: PropTypes.string
};

export default Footer;
