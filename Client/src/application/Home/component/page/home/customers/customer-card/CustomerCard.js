import React from 'react';
import {Card} from "react-bootstrap";
import styles from "./customer-card.module.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome/index";
import {faQuoteLeft, faQuoteRight} from "@fortawesome/free-solid-svg-icons/index";
import PropTypes from 'prop-types';

const CustomerCard = (props) => {
    return (
        <Card className={styles.card}>
            <Card.Header className={styles.bg_gradient} style={{background: props.background}}/>
            <img className={styles.avatar} src={props.img} alt='customer'/>
            <Card.Body>
                <h4 className={styles.name}>{props.name}</h4>
                <h1 className={styles.title}>{props.title}</h1>
                <div className={styles.divider}/>
                <blockquote className={styles.quote}>
                    <FontAwesomeIcon className={styles.quote_icon} size="1x"
                                     icon={faQuoteLeft}/>
                    {props.review}
                    <FontAwesomeIcon className={styles.quote_icon} size="1x"
                                     icon={faQuoteRight}/>
                </blockquote>
            </Card.Body>
        </Card>
    );
};

CustomerCard.propTypes = {
    background: PropTypes.string,
    img: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    review: PropTypes.string.isRequired
};

export default CustomerCard;
