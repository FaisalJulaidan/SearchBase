import React from 'react';
import {Button, Col, Container, Image, Row} from "react-bootstrap";
import styles from "./intro.module.css";
import {Bounce} from "react-reveal";
import {Link} from "react-router-dom";
import TextTransition from "react-text-transition";

class Intro extends React.Component {

    titles = ['Automate', 'Analyse', 'Empower'];
    timerIntervalID = 0;

    state = {activeTitleIndex: 0};

    componentDidMount() {
        this.timerIntervalID = setInterval(() => {
            let activeTitleIndex = this.state.activeTitleIndex + 1;
            if (activeTitleIndex >= this.titles.length)
                activeTitleIndex = 0;
            this.setState({activeTitleIndex: activeTitleIndex});
        }, 3000);
    }

    componentWillUnmount() {
        clearInterval(this.timerIntervalID);
    }

    render() {
        return (
            <Container>
                <Row>
                    <Col className={styles.text_col} xs={12} md={5} lg={5}>
                        <Bounce left big>
                            <TextTransition className={styles.title_transient}
                                            text={this.titles[this.state.activeTitleIndex]}/>
                            <h2 className={styles.title}>
                                your recruitment process and Grow
                            </h2>
                            <h3 className={styles.subtitle}>Delivering Powerful Automation to Recruiters</h3>
                            <Button variant="outline-light" className={styles.button}>
                                <Link to="/get-started" style={{textDecoration: 'none'}}>Book a demo</Link>
                            </Button>
                        </Bounce>
                    </Col>
                    <Col xs={12} md={7} lg={7}>
                        <div className={styles.image_wrapper}>
                            <Image className={styles.image} src="assets/img/home/destinations.svg"/>
                        </div>
                    </Col>
                </Row>
            </Container>
        );
    }

}

export default Intro;
