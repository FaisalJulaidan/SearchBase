import React from 'react';
import styles from './slider.module.css'
import {Col, Container, Row} from "react-bootstrap";
import AliceCarousel from 'react-alice-carousel';
import "react-alice-carousel/lib/alice-carousel.css";
import itemsJSON from "./items.json";
import SliderItem from "./slider-item/SliderItem";
import NavItem from "./nav-item/NavItem";

class Slider extends React.Component {

    state = {
        currentSliderIndex: 0,
        sliderDotsDisabled: window.innerWidth >= 768,
        items: itemsJSON
    };

    sliderItems = this.state.items.map((item, i) => {
        return (
            <SliderItem key={i} intro={item.intro} text={item.text} image={item.image}/>
        );
    });

    navItems = this.state.items.map((item, i) => {
        return (
            <NavItem key={i} id={i} title={item.title} onClick={() => {
                this.setState({currentSliderIndex: i})
            }}/>
        );
    });

    render() {
        return (
            <div className={styles.wrapper}>
                <Container>
                    <Row>
                        <Col className={styles.col_intro}>
                            <h1 className={styles.title}>How it works.</h1>
                            <h4 className={styles.subtitle}>Customized workflows to connect with talent across the full
                                candidate life cycle.</h4>
                        </Col>
                    </Row>
                    <Row>
                        <Col className={styles.col_nav}>
                            {this.navItems}
                        </Col>
                    </Row>
                    <Row>
                        <Col className={styles.col_slider}>
                            <AliceCarousel
                                infinite
                                autoPlay
                                autoPlayInterval={5000}
                                duration={1000}
                                stopAutoPlayOnHover={false}
                                slideToIndex={this.state.currentSliderIndex}
                                dotsDisabled={this.state.sliderDotsDisabled}
                                buttonsDisabled
                                items={this.sliderItems}
                                responsive={{0: {items: 1}}}
                                stagePadding={{paddingLeft: 0, paddingRight: 0}}/>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }


}

export default Slider;
