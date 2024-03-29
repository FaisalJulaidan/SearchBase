import React from 'react';
import styles from './integrations.module.css'
import integrations from './integrations.json'
import "react-alice-carousel/lib/alice-carousel.css";
import {Container, Col, Image, Row} from "react-bootstrap";
import {getLink} from "helpers";

class Integrations extends React.Component {

    items = integrations.map((item, i) => {
        return (
            <Col key={i} className={styles.col_item}>
                <Image className={styles.image}
                       src={getLink(item.image)}/>
                <h1 id="title" className={styles.title}>{item.title}</h1>
            </Col>
        );
    });

    render() {

        return (
            <Container id={this.props.id}>
                <Row>
                    <Col className={styles.col_text}>
                        <h1 className={styles.title}>Integrated with the platforms you are familiar with</h1>
                        <hr/>
                    </Col>
                </Row>
                <Row>
                    {this.items}
                </Row>
            </Container>
        );
    }
}

export default Integrations;
