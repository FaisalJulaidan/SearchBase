import React, {Component} from 'react';
import styles from './job-offer-item.module.css'
import {Image} from "react-bootstrap";
import PropTypes from 'prop-types';
import {getLink} from "helpers";

class JobOfferItem extends Component {
    render() {
        return (
            <div className={styles.wrapper}>
                <Image fluid className={styles.image} src={"/images/home/home/designer.svg"}/>
                <div className={styles.text_wrapper}>
                    <h1 className={styles.title}>Python Developer</h1>
                    <h1 className={styles.text}>Location: London, UK</h1>
                    <h1 className={styles.text}>Salary: 250 GBP</h1>
                    <h1 className={styles.text}>Remote candidates also can apply, but the salary would be cut by
                        10%</h1>
                </div>
                <h1 className={styles.button}>Apply</h1>
            </div>
        );
    }
}

JobOfferItem.propTypes = {};

export default JobOfferItem;
