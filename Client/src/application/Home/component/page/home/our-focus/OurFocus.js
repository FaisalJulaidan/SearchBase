import React from 'react';
import styles from "./our-focus.module.css";
import {Col, Container, Row, Image} from "react-bootstrap";
// import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCogs, faSms, faComments} from "@fortawesome/free-solid-svg-icons";
import {Flip} from "react-reveal";
import {getLink} from "helpers";

class OurFocus extends React.Component {

    items = [
        {
            img: getLink('/images/home/home/chat.png'),
            icon: faComments,
            title: 'Engagement',
            text: 'We have built powerful and highly intuitive engagement routes that keep you updated about your candidates.'
        },
        {
            img: getLink('/images/home/home/score.png'),
            icon: faSms,
            title: 'Candidate Activation',
            text: 'Our platform has helped Recruiters save time, and automated their candidate outreach. ' +
                'Allowing them to build talent pools much faster.'
        },
        {
            img: getLink('/images/home/home/airplane.png'),
            icon: faCogs,
            title: 'Autopilot',
            text: 'Have total control over your automation and take care of mundane tasks within seconds. ' +
                'Use your time to build stronger relationships and make placements faster.'
        }
    ];

    state = {
        items: this.items.map((item, i) => {
            return (
                <Col key={i} xs={12} sm={{span: 8, offset: 2}} md={{span: 4, offset: 0}} className={styles.col_item}>
                    <Flip fraction={1} bottom>
                        <div className={styles.image_wrapper}>
                            <Image className={styles.image} src={item.img}/>
                        </div>
                        {/*<FontAwesomeIcon className={styles.icon} size='6x' icon={item.icon}/>*/}
                    </Flip>
                    <h1 className={styles.title}>{item.title}</h1>
                    <hr/>
                    <p className={styles.text}>{item.text}</p>
                </Col>
            );
        })
    };

    render() {
        return (
            <Container id={this.props.id}>
                <Row>
                    <Col className={styles.col_header}>
                        <h1 className={styles.title}>Do More, With Less</h1>
                    </Col>
                </Row>
                <Row>
                    {this.state.items}
                </Row>
            </Container>
        );
    }
}

export default OurFocus;
