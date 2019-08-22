import React, {Component} from 'react';
import {Col, Image, Row} from "react-bootstrap";
import styles from './slider-item.module.css'
import PropTypes from "prop-types";

class SliderItem extends Component {

    state = {
        intro: this.props.intro,
        text: this.props.text,
        image: this.props.image
    };

    render() {
        return (
            <Row className={styles.center}>
                <Col xs={{span: 12}} md={{span: 6}} lg={{span: 5, offset: 1}}>
                    <h1 className={styles.title}>{this.state.title}</h1>
                    <span>{this.state.text}</span>
                </Col>
                <Col xs={{span: 12}} md={{span: 6, offset: 0}} lg={{span: 5, offset: 0}}>
                    <Image className={styles.image} fluid src={this.state.image}/>
                </Col>
            </Row>
        );
    }
}

SliderItem.propTypes = {
    intro: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
    image: PropTypes.string.isRequired,
};

export default SliderItem;
