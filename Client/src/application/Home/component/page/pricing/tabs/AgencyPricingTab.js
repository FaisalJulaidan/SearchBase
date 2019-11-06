import React from 'react';
import styles from './agency-pricing-tab.module.css';
import {Link} from "react-router-dom";
import {Button, Col, Row, Card} from "react-bootstrap";
import pricingJSON from "../pricing.json";
import PricingItem from "../pricing-item/PricingItem";

const AgencyPricingTab = () => {

    let pricing = pricingJSON.map((plan, key) => {
        return (
            <Col className={styles.col_item} xs={{span: 10, offset: 1}} sm={{span: 8, offset: 2}}
                 md={{span: 4, offset: 0}}
                 key={key}>
                <PricingItem id={plan.id} plan={plan}/>
            </Col>
        );
    });
    return (
        <div className={styles.wrapper}>
            <div>
                <Card className={styles.card}>
                    <Card.Body>
                        <Row>
                            {pricing}
                        </Row>
                        <Row>
                            <Col className={styles.col_compare_button}>
                                <Button variant="outline-light" className={styles.button}>SEE FULL COMPARISON
                                    TABLE</Button>
                            </Col>
                        </Row>
                    </Card.Body>
                </Card>
            </div>
            <div className={styles.table_wrapper}>
                <h1>Full Plan Comparison</h1>
                <hr/>
                <h4>Interested in a strategic partner to help you roll out automatic recruitment? Check out our
                    <Link to="#">Enterprise</Link> solution</h4>
            </div>
        </div>
    );
};

export default AgencyPricingTab;