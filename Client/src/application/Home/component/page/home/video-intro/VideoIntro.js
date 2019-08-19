import React from 'react';
import {Col, Container, Row} from "react-bootstrap";
import styles from "./video-intro.module.css";
import ReactPlayer from "react-player";
import VideoWrapper from "./video-wrapper/VideoWrapper";
import {Fade} from "react-reveal";
import {faArrowCircleRight} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {Link} from "react-router-dom";
import {getLink} from "helpers";

class VideoIntro extends React.Component {

    state = {
        text: {
            intro: 'Seamless Experience',
            title: 'Capture candidates, in seconds',
            text: 'By interacting with candidates using Chatbots,\n' +
                'you are working at times of Convenience for the Candidates, in a Confidential\n' +
                'Environment. With direct interaction between you and candidates, your business can\n' +
                'make Connections and build Highly Descriptive Candidate Profiles in Seconds.',
        }
    };

    render() {
        let fadeAnim = {};
        if (window.innerWidth > 767.98) fadeAnim["left"] = true; else fadeAnim["bottom"] = true;
        return (
            <Container id={this.props.id}>
                <Row className={styles.center}>
                    <Col xs={{span: 8, offset: 2, order: 1}} md={{span: 6, offset: 0, order: 1}}
                         lg={{span: 4, offset: 1, order: 1}}>
                        <ReactPlayer playing pip loop wrapper={VideoWrapper}
                                     url={getLink("/static/images/sb-video.mp4")}/>
                    </Col>
                    <Col xs={{span: 12, order: 2}} sm={{span: 10, order: 2, offset: 1}} md={{span: 6, offset: 0}}
                         lg={{span: 6, offset: 1}}>
                        <div className={styles.text_section}>
                            <Fade {...fadeAnim} big>
                                <h1 className={styles.intro}>{this.state.text.intro}</h1>
                                <h3 className={styles.title}>{this.state.text.title}</h3>
                                <h6 className={styles.text}>{this.state.text.text}</h6>
                                <Link to="/how-it-works" className={styles.button}>
                                    Read How it works <FontAwesomeIcon className={styles.icon}
                                                                       icon={faArrowCircleRight}/>
                                </Link>
                            </Fade>
                        </div>
                    </Col>
                </Row>
            </Container>
        )
            ;
    }
}

export default VideoIntro;
