import React from 'react';
import {Col, Container, Row,Image} from "react-bootstrap";
import styles from "./message-intro.module.css";
import {Fade} from "react-reveal";
import {faArrowCircleRight} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {getLink} from "helpers";
import {Link} from "react-router-dom";


class MessageIntro extends React.Component {

    state = {
        text: {
            intro: 'Seamless Experience',
            title: 'Capture candidates, in seconds',
            text: 'By interacting with candidates using chatbots,\n' +
                'you are working at times of convenience for the candidates, in a confidential\n' +
                'environment. With direct interaction between you and candidates, your business can\n' +
                'make connections and build highly descriptive candidate profiles in seconds.',
        }
    };

    render() {

        let fadeAnim = {};
        if (window.innerWidth > 767.98) fadeAnim["left"] = true; else fadeAnim["bottom"] = true;
        return (
            <Container id={this.props.id}>
                <Row className={styles.center}>
                    <Col xs={12} md={6}>
                        <div className={styles.image_wrapper}>
                            <Image className={styles.image}
                                   src={"/images/home/home/data-trends.png"}/>
                        </div>
                    </Col>
                    <Col xs={{span: 12, order: 2}} sm={{span: 10, order: 2, offset: 1}} md={{span: 6, offset: 0}}
                         lg={{span: 6}}>
                        <div className={styles.text_section}>
                            <Fade {...fadeAnim} big>
                                <h1 className={styles.intro}>{this.state.text.intro}</h1>
                                <h3 className={styles.title}>{this.state.text.title}</h3>
                                <h6 className={styles.text}>{this.state.text.text}</h6>
                                <Link to="/how-it-works" className={styles.button}>
                                    How it works <FontAwesomeIcon className={styles.icon}
                                                                       icon={faArrowCircleRight}/>
                                </Link>
                            </Fade>
                        </div>
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default MessageIntro;
