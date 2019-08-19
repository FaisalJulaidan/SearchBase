import React, {Component} from 'react';
import styles from './descriptive-section.module.css'
import PropTypes from 'prop-types';
import {Col, Container, Image, Row} from "react-bootstrap";
import {getLink} from "helpers";

class DescriptiveSection extends Component {

    render() {

        let texts = this.props.texts.map((text, i) => {
            return (
                <p key={i} className={styles.text}>
                    <br/>
                    {text}
                </p>
            );
        });

        return (
            <div id={this.props.id} style={this.props.noBackground ? {background: 'none'} : {}}
                 className={styles.wrapper}>
                <Container>
                    <Row>
                        <Col md={6}>
                            <h3 className={styles.intro}>
                                {this.props.intro}
                            </h3>
                            <h1 className={styles.title}>
                                {this.props.title}
                            </h1>
                            {texts}
                        </Col>
                        <Col md={6}>
                            <div className={styles.image_wrapper}>
                                <Image className={styles.image} fluid src={getLink(this.props.image)}/>
                            </div>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

DescriptiveSection.propTypes = {
    intro: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    texts: PropTypes.arrayOf(PropTypes.string).isRequired,
    image: PropTypes.string.isRequired,
    noBackground: PropTypes.bool,
};

export default DescriptiveSection;
