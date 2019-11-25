import React from 'react';
import styles from './pricing.module.css';
import {Col, Container, Row, Nav, Tab} from "react-bootstrap";
import Layout from "../../../hoc/layout/Layout";
import {BREAKPOINTS, WEBSITE_TITLE} from "../../../../../constants/config";
import LeadGenerationPricingTab from "./tabs/LeadGenerationPricingTab";
import AutomationPricingTab from "./tabs/AutomationPricingTab";
import EnterprisePricingTab from "./tabs/EnterprisePricingTab";

class Pricing extends React.Component {

    state = {
        activeTab: 'lead-generation'
    };

    componentDidMount() {
        document.title = "Pricing | " + WEBSITE_TITLE;
        if (["lead-generation", "automation", "enterprise"].includes(this.props.location.hash.replace("#", ""))) {
            this.setState({activeTab: this.props.location.hash.replace("#", "")});
        }
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.location.hash !== prevProps.location.hash &&
            ["lead-generation", "automation", "enterprise"].includes(this.props.location.hash.replace("#", ""))) {
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
                                        <Nav.Link eventKey="lead-generation"
                                                  style={this.state.activeTab === 'lead-generation' ? {
                                                      fontWeight: '900',
                                                      color: "#9254de"
                                                  } : {}}>
                                            Lead Generation
                                        </Nav.Link>
                                    </Nav.Item>
                                    <Nav.Item className={styles.tab}>
                                        <Nav.Link eventKey="automation"
                                                  style={this.state.activeTab === 'automation' ? {
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
                                    <Tab.Pane eventKey="lead-generation">
                                        <LeadGenerationPricingTab/>
                                    </Tab.Pane>
                                    <Tab.Pane eventKey="automation">
                                        <AutomationPricingTab/>
                                    </Tab.Pane>
                                    <Tab.Pane eventKey="enterprise">
                                        <EnterprisePricingTab/>
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
