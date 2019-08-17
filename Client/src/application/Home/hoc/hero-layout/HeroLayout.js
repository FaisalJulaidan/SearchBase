import React from 'react';
import styles from './hero-layout.module.css';
import PropTypes from "prop-types";
import {Container, Row, Col} from "react-bootstrap";
import {ReactComponent as Wave} from './wave.svg';

const HeroLayout = (props) => {
    return (
        <div>
            <div className={styles.hero}>
                <Container>
                    <Row>
                        <Col className={styles.text_wrapper}>
                            <h1 className={styles.title}>{props.title}</h1>
                            <h1 className={styles.subtitle}>{props.subtitle}</h1>
                        </Col>
                    </Row>
                </Container>
                <Wave className={styles.wave}/>
            </div>
            {props.children}
        </div>
    );
};

HeroLayout.propTypes = {
    title: PropTypes.string.isRequired,
    subtitle: PropTypes.string.isRequired,
    background: PropTypes.string
};

export default HeroLayout;
