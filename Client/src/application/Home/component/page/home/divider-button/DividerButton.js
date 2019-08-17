import React from 'react';
import {Col, Container, Row} from "react-bootstrap";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome/index";
import {faChevronCircleDown} from "@fortawesome/free-solid-svg-icons/index";
import styles from './divider-button.module.css'
import PropTypes from 'prop-types';
import {Link as ScrollLink} from "react-scroll/modules";

const DividerButton = (props) => {
    return (
        <ScrollLink to={props.scrollTo} smooth={true} offset={-100} duration={1000}>
            <Container>
                <Row>
                    <Col md={true} className={styles.center}>
                        <div className={styles.pointer}>
                            <FontAwesomeIcon size="3x" color="#dfdfdf" icon={faChevronCircleDown}/>
                        </div>
                    </Col>
                </Row>
            </Container>
        </ScrollLink>
    );
};

DividerButton.propTypes = {
    scrollTo: PropTypes.string
};

export default DividerButton;
