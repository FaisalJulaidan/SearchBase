import React from 'react';
import styles from './pricing-item.module.css';
import PropTypes from "prop-types";
import {Link} from "react-router-dom";
import Button from "react-bootstrap/Button";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck} from "@fortawesome/free-solid-svg-icons";

const PricingItem = (props) => {

    let items = props.plan?.items?.map((item, key) => {
        return <li key={key}><FontAwesomeIcon color="#4CAF50" size="1x" icon={faCheck} className={styles.icon}/>{item}
        </li>
    });

    return (
        <div className={styles.wrapper}>
            <h1 className={styles.title}>{props.plan?.title}</h1>
            <hr/>
            {!props?.hide_subtitle && <h1 className={styles.subtitle}>{props.plan?.subtitle}</h1>}
            <h4 className={styles.price}>{props.plan?.price}</h4>
            <h4 className={styles.price_subtitle}>{props.plan?.price_subtitle}</h4>
            <Link to={`/order-plan?plan=${props.id}`} style={{width: 'fit-content'}}>
                <Button variant="outline-light" className={styles.button}>Order Now</Button>
            </Link>
            <hr/>
            <ul className={styles.list}>
                {items}
            </ul>
        </div>
    );
};

PricingItem.propTypes = {
    plan: PropTypes.shape({
        title: PropTypes.string.isRequired,
        subtitle: PropTypes.string.isRequired,
        price: PropTypes.string.isRequired,
        price_subtitle: PropTypes.string,
        icon: PropTypes.string,
        items: PropTypes.arrayOf(PropTypes.string)
    }),
    hide_subtitle: PropTypes.bool
};

export default PricingItem;