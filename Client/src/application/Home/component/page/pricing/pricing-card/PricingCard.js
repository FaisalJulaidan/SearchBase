import React from 'react';
import styles from './pricing-card.module.css';
import PropTypes from "prop-types";
import {Card} from "react-bootstrap";
import Button from "react-bootstrap/Button";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import {faHome,faBuilding,faCity} from "@fortawesome/free-solid-svg-icons";
library.add(faHome,faBuilding,faCity);
const PricingCard = (props) => {

    let items = props.items?.map((item,key)=>{
        return <li key={key}>{item}</li>
    });

    return (
            <Card className={styles.card}>
                <Card.Body className={styles.body}>
                    <FontAwesomeIcon className={styles.icon} size="4x" icon={props.icon}/>
                    <h1 className={styles.title}>{props.title}</h1>
                    <hr/>
                    <h1 className={styles.subtitle}>{props.subtitle}</h1>
                    <h4 className={styles.price}>{props.price}</h4>
                    <ul className={styles.list}>
                        {items}
                    </ul>
                    <Button variant="outline-light" className={styles.button} block>Order now</Button>
                </Card.Body>
            </Card>
    );
};

PricingCard.propTypes = {
    title: PropTypes.string.isRequired,
    subtitle: PropTypes.string.isRequired,
    price: PropTypes.string.isRequired,
    icon: PropTypes.string,
    items: PropTypes.arrayOf(PropTypes.string)
};

export default PricingCard;
