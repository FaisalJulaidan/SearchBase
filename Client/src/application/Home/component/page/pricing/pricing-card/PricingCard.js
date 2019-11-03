import React from 'react';
import styles from './pricing-card.module.css';
import PropTypes from "prop-types";
import {Link} from "react-router-dom";
import {Card} from "react-bootstrap";
import Button from "react-bootstrap/Button";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {library} from '@fortawesome/fontawesome-svg-core';
import {faHome, faBuilding, faCity} from "@fortawesome/free-solid-svg-icons";

library.add(faHome, faBuilding, faCity);
const PricingCard = (props) => {

    let items = props.plan?.items?.map((item, key) => {
        return <li key={key}>{item}</li>
    });

    return (
        <Card className={styles.card}>
            <Card.Body className={styles.body}>
                {/*<FontAwesomeIcon className={styles.icon} size="3x" icon={props.icon}/>*/}
                <h1 className={styles.title}>{props.plan?.title}</h1>
                <hr/>
                <h1 className={styles.subtitle}>{props.plan?.subtitle}</h1>
                <h4 className={styles.price}>{props.plan?.price}</h4>
                <h4 className={styles.price_subtitle}>{props.plan?.price_subtitle}</h4>
                <Button as={Link} to={`/order-plan?plan=${props.id}`} variant="outline-light" className={styles.button}>Order Now</Button>
                <hr/>
                <ul className={styles.list}>
                    {items}
                </ul>
            </Card.Body>
        </Card>
    );
};

PricingCard.propTypes = {
    plan : PropTypes.shape({
        title: PropTypes.string.isRequired,
        subtitle: PropTypes.string.isRequired,
        price: PropTypes.string.isRequired,
        price_subtitle: PropTypes.string,
        icon: PropTypes.string,
        items: PropTypes.arrayOf(PropTypes.string)
    })
};

export default PricingCard;
