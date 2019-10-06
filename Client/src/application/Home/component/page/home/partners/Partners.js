import React from 'react';
import styles from './partners.module.css'
import {Image,Col, Container, Row} from "react-bootstrap";
import partners from './partners.json'
import "react-alice-carousel/lib/alice-carousel.css";
import {getLink} from "helpers";

class Partners extends React.Component {

    items = partners.map((item, i) => {
        return (
            <Col key={i} className={styles.col_item}>
                <a href={item.link} target="_blank">
                    <Image className={styles.image}
                           src={getLink(item.image)}/>
                </a>
                {/*<h1 id="title" className={styles.title}>{item.title}</h1>*/}
            </Col>
        );
    });

    render() {

        return (
            <Container id={this.props.id}>
                <Row>
                    <Col className={styles.col_text}>
                        <h1 className={styles.title}>Trusted by over 100+ Recruitment Companies</h1>
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

export default Partners;
