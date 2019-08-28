import React from 'react';
import styles from './feature-item.module.css';
import PropTypes from 'prop-types';
import {Col, Container, Image, Row} from "react-bootstrap";
import {Fade} from "react-reveal";

class FeatureItem extends React.Component {

    state = {
        title: this.props.title,
        subtitle: this.props.subtitle,
        text: this.props.text,
        img: this.props.img,
        textPosition: this.props.textPosition,
    };


    textCol() {
        // let fadeAnim = {};
        // if (this.state.textPosition) {
        //     fadeAnim["right"] = true;
        // } else {
        //     fadeAnim["left"] = true;
        // }

        return (
            <Col xs={{span: 12, order: 1}} md={{span: 7, order: 0}} lg={6} className={styles.text_col}>
                {/*<Fade {...fadeAnim} fraction={1}>*/}
                    <h1 className={styles.title}>{this.state.title}</h1>
                    <h5 className={styles.subtitle}>{this.state.subtitle}</h5>
                    <p className={styles.text}>{this.state.text}</p>
                {/*</Fade>*/}
            </Col>
        );
    }

    imageCol() {
        return (
            <Col xs={{span: 12, order: 2}} md={{span: 5, order: 0}} lg={6} className={styles.image_col}>
                <Fade>
                    <div className={styles.image_wrapper}>
                        <Image className={styles.image} fluid src={this.state.img}/>
                    </div>
                </Fade>
            </Col>
        );
    }

    render() {
        return (
            <Container>
                <Row>
                    {this.state.textPosition ? this.imageCol() : this.textCol()}
                    {this.state.textPosition ? this.textCol() : this.imageCol()}
                </Row>
            </Container>
        );
    }
}

FeatureItem.propTypes = {
    title: PropTypes.string.isRequired,
    subtitle: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
    img: PropTypes.string.isRequired,
    textPosition: PropTypes.bool.isRequired
};

export default FeatureItem;
