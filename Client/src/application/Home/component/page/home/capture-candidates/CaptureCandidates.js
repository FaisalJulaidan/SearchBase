import React from 'react';
import {Col, Container, Image, Row} from "react-bootstrap";
import styles from "./capture-candidates.module.css";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faArrowRight} from "@fortawesome/free-solid-svg-icons";

const CaptureCandidates = (props) => {
    return (
        <Container id={props.id}>
            <Row className={styles.row}>
                <Col md={8} className={styles.text_col}>
                    <h1 className={styles.title}>Build Talent Pools, Faster than before</h1>
                </Col>
                <Col xs={{span: 8, offset: 2}} lg={{span: 4, offset: 4}}>
                    <div className={styles.image_wrapper}>
                        <Image className={styles.image} fluid src="assets/img/home/speed.svg"/>
                    </div>
                </Col>
                <Col md={8} className={styles.text_col}>
                    <h1 className={styles.text}>With direct communication between you and candidates, your business can
                        collect a wealth of highly descriptive candidate profiles in seconds.</h1>
                    <Link  to="/how-it-works" className={styles.button}>
                       Tell me more <FontAwesomeIcon className={styles.icon} icon={faArrowRight}/>
                    </Link>
                </Col>
            </Row>
        </Container>
    );
};

export default CaptureCandidates;
