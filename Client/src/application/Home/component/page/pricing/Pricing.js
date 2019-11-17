import React from 'react';
import styles from './pricing.module.css';
import {Col, Container, Row, Nav, Tab} from "react-bootstrap";
import Layout from "../../../hoc/layout/Layout";
import {BREAKPOINTS, WEBSITE_TITLE} from "../../../../../constants/config";
import AgencyPricingTab from "./tabs/AgencyPricingTab";
import InHousePricingTab from "./tabs/InHousePricingTab";
import EnterprisePricingTab from "./tabs/EnterprisePricingTab";

class Pricing extends React.Component {

    state = {
        activeTab: 'agency'
    };

    componentDidMount() {
        document.title = "Pricing | " + WEBSITE_TITLE;
        if (["agency", "enterprise", "in-house"].includes(this.props.location.hash.replace("#", ""))) {
            this.setState({activeTab: this.props.location.hash.replace("#", "")});
        }
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.location.hash !== prevProps.location.hash &&
            ["agency", "enterprise", "in-house"].includes(this.props.location.hash.replace("#", ""))) {
            this.setState({activeTab: this.props.location.hash.replace("#", "")});
        }
    }

    render() {
        return (
            <Layout>
                <div className={styles.hero}>
                    <Container>
                        <Row>
                            <Col className={styles.text_wrapper}>
                                <h1 className={styles.title}>Boost candidates interaction and automate every mundane
                                    task in
                                    your business.</h1>
                            </Col>
                        </Row>
                    </Container>
                </div>
                <Container className={styles.content}>
                    <Tab.Container activeKey={this.state.activeTab}
                                   onSelect={key => this.props.history.push(`/pricing#${key}`)}>
                        <Row>
                            <Col>
                                <Nav variant="tabs" fill justify
                                     className={`${styles.tabs} ${(window.innerWidth < BREAKPOINTS.sm) ? 'flex-column' : ''}`}
                                     onSelect={() => {
                                     }}>
                                    <Nav.Item className={styles.tab}>
                                        <Nav.Link eventKey="agency"
                                                  style={this.state.activeTab === 'agency' ? {
                                                      fontWeight: '900',
                                                      color: "#9254de"
                                                  } : {}}>
                                            Basic
                                        </Nav.Link>
                                    </Nav.Item>
                                    <Nav.Item className={styles.tab}>
                                        <Nav.Link eventKey="in-house"
                                                  style={this.state.activeTab === 'in-house' ? {
                                                      fontWeight: '900',
                                                      color: "#9254de"
                                                  } : {}}>
                                            Automation
                                        </Nav.Link>
                                    </Nav.Item>
                                    <Nav.Item className={styles.tab}>
                                        <Nav.Link eventKey="enterprise"
                                                  style={this.state.activeTab === 'enterprise' ? {
                                                      fontWeight: '900',
                                                      color: "#9254de"
                                                  } : {}}>
                                            Enterprise
                                        </Nav.Link>
                                    </Nav.Item>
                                </Nav>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <Tab.Content>
                                    <Tab.Pane eventKey="agency">
                                        <AgencyPricingTab/>
                                    </Tab.Pane>
                                    <Tab.Pane eventKey="enterprise">
                                        <EnterprisePricingTab/>
                                    </Tab.Pane>
                                    <Tab.Pane eventKey="in-house">
                                        <InHousePricingTab/>
                                    </Tab.Pane>
                                </Tab.Content>
                            </Col>
                        </Row>
                    </Tab.Container>
                </Container>
            </Layout>
        );
    }
}

export default Pricing;
