import React from 'react';
import {Button, Col, Container, Row} from "react-bootstrap";
import styles from "./why-wait.module.css";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCloud} from "@fortawesome/free-solid-svg-icons";
import Fade from 'react-reveal/Fade';
import {animateScroll as scroll} from "react-scroll";

const WhyWait = (props) => {
    return (
        <Container id={props.id}>
            <Row>
                <Col md={{span: 10, offset: 1}} lg={{span: 10, offset: 1}}>
                    <div className={styles.wrapper}>
                        <div className={styles.logo_wrapper}>
                            <FontAwesomeIcon className={styles.logo}
                                             size="5x"
                                             color="#9254de"
                                             icon={faCloud}
                                             onClick={() => scroll.scrollToTop()}/>
                        </div>
                        <div className={styles.text}>
                            <h1>Power up your recruitment business</h1>
                            <h1>with</h1>
                            <h1 style={{color: '#9254de'}}><b>SearchBase</b></h1>
                        </div>
                        <Fade duration={1500} fraction={1}>
                            <Link to="/get-started">
                                <Button className={styles.button} variant="outline-light">Book a demo</Button>
                            </Link>
                        </Fade>
                    </div>
                </Col>
            </Row>
        </Container>
    );
};

export default WhyWait;
