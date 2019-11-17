import React from 'react';
import styles from './agency-pricing-tab.module.css';
import {Link} from "react-router-dom";
import {Button, Col, Row, Card} from "react-bootstrap";
import pricingJSON from "../pricingAgency.json";
import PricingItem from "../pricing-item/PricingItem";
import PlansTable from "../plans-table/PlansTable";

import {scroller} from "react-scroll";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faChevronRight} from "@fortawesome/free-solid-svg-icons";

const AgencyPricingTab = () => {

    let pricing = pricingJSON.map((plan, key) => {
        return (
            <Col className={styles.col_item} xs={{span: 10, offset: 1}} sm={{span: 8, offset: 2}}
                 md={{span: 4, offset: 0}}
                 key={key}>
                <PricingItem id={plan.id} plan={plan} hide_subtitle={true}/>
            </Col>
        );
    });
    return (
        <div className={styles.wrapper}>
            <div>
                <Card className={styles.card}>
                    <Card.Body className={styles.pricing_card_body}>
                        <Row>
                            {pricing}
                        </Row>
                        <Row className={styles.row_buttons}>
                            <Col xs={{span: 10, offset: 1}} md={{span:6,offset:0}} lg={{span: 4, offset: 2}} className={styles.col_button}>
                                <Button variant="outline-light" className={styles.compare_button}
                                        onClick={() => {
                                            scroller.scrollTo("plans-table", {
                                                offset: -100, duration: 1000,
                                                delay: 100, smooth: true,
                                            })
                                        }}>
                                    see full plan comparison 👀
                                </Button>
                            </Col>
                            <Col xs={{span: 10, offset: 1}} md={{span:6,offset:0}} lg={4} className={styles.col_button}>
                                <Button as={Link} to="#enterprise" onClick={() => window.scrollTo(0, 250)}
                                        variant="primary" className={styles.enterprise_button}>see our enterprise
                                    solution</Button>
                            </Col>
                        </Row>
                    </Card.Body>
                </Card>
            </div>
            <div>
                <Row>
                    <Col xs={12} lg={6} className={styles.col_card}>
                        <Card className={styles.card}>
                            <Card.Body className={styles.product_card_body}>
                                <div>
                                    <h1>CHATBOTS</h1>
                                    <p>Our chatbots help you spend less time screening and qualifying candidates.</p>
                                </div>
                                <Link to="/how-it-works#chatbot">learn more<FontAwesomeIcon className={styles.icon}
                                                                                            icon={faChevronRight}/>
                                </Link>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col xs={12} lg={6} className={styles.col_card}>
                        <Card className={styles.card}>
                            <Card.Body className={styles.product_card_body}>
                                <div>
                                    <h1>SMS outreach</h1>
                                    <p>Candidates may have access to the internet, so we have developed a solution that works, offline and online.</p>
                                </div>
                                <Link to="/how-it-works#sms">learn more<FontAwesomeIcon className={styles.icon}
                                                                                        icon={faChevronRight}/>
                                </Link>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </div>
            <div>
                <Row>
                    <Col md={{span: 10, offset: 1}} className={styles.col_demo_text}>
                        <h1>Join the 100+ businesses which are using SearchBase to connect with their customers.</h1>
                    </Col>
                </Row>
                <Row>
                    <Col className={styles.col_demo_button}>
                        <Button as={Link} to={"/get-started"} variant="primary" className={styles.demo_button}>Get a
                            demo</Button>
                    </Col>
                </Row>
            </div>
            <div className={styles.table_wrapper} id={"plans-table"}>
                <h1>Full Plan Comparison</h1>
                <hr/>
                <h4>Interested in a strategic partner to help you roll out automatic recruitment? Check out our
                    <Link to="#enterprise" onClick={() => window.scrollTo(0, 250)}>Enterprise</Link>solution</h4>
                <PlansTable className={styles.plans_table}/>
            </div>
        </div>
    );
};

export default AgencyPricingTab;