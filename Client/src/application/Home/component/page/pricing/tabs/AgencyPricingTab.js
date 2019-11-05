import React from 'react';
import styles from './agency-pricing-tab.module.css';
import {Container, Col, Row, Card} from "react-bootstrap";
import pricingJSON from "../pricing";
import PricingItem from "../pricing-item/PricingItem";

const AgencyPricingTab = () => {

    let pricing = pricingJSON.map((plan, key) => {
        return (
            <Col className={styles.col_card} xs={{span: 10, offset: 1}} sm={{span: 8, offset: 2}}
                 md={{span: 4, offset: 0}}
                 key={key}>
                <PricingItem id={plan.id} plan={plan}/>
            </Col>
        );
    });
    return (
        <Container>
            <Row>
                <Card>
                    <Card.Body>
                        <Row>
                            {pricing}
                        </Row>
                    </Card.Body>
                </Card>
            </Row>
        </Container>
    );
};

export default AgencyPricingTab;