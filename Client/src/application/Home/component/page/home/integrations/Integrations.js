import React from 'react';
import styles from './integrations.module.css'
import integrations from './integrations.json'
import AliceCarousel from 'react-alice-carousel';
import "react-alice-carousel/lib/alice-carousel.css";
import {Col, Container, Image, Row} from "react-bootstrap";

class Integrations extends React.Component {

    state = {
        items: integrations.map((item, i) => {
            return (
                <div className={styles.center}>
                    <Image key={i} className={styles.image} src={item.image}/>
                </div>
            );
        })
    };

    render() {

        return (
            <Container id={this.props.id}>
                <Row>
                    <Col className={styles.col}>
                        <h1 className={styles.title}>Integrated with the platforms you are familiar with</h1>
                        <hr/>
                        <AliceCarousel
                            dotsDisabled
                            buttonsDisabled
                            keysControlDisabled
                            swipeDisabled
                            infinit={false}
                            items={this.state.items}
                            responsive={{0: {items: 7}, 1024: {items: 7}}}
                            stagePadding={{paddingLeft: 0, paddingRight: 0}}/>
                    </Col>
                </Row>
            </Container>
        );
    }
}

export default Integrations;
