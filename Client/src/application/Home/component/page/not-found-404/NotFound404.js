import React from 'react';
import styles from './not-found-404.module.css';
import {WEBSITE_TITLE} from '../../../../../constants/config';
import {Button, Col, Container, Row} from "react-bootstrap";
import {Link} from "react-router-dom";
import Layout from "../../../hoc/layout/Layout";

const MyComponent = () => {

    document.title = WEBSITE_TITLE;

    return (
        <Layout>
            <Container className={styles.container}>
                <Row>
                    <Col md={{span: 1, offset: 3}}>
                        <span className={styles.emoji}>:(</span>
                    </Col>
                    <Col md={6}>
                        <h1 className={styles.title}>404 - PAGE NOT FOUND</h1>
                        <h4 className={styles.desc}>The page you are looking for might have been removed, had its name
                            changed, or is temporarily unavailable.
                        </h4>
                        <Button variant="outline-info" className={styles.button}> <Link to="/"
                                                                                        style={{textDecoration: 'none'}}>Home
                            Page</Link></Button>
                    </Col>
                </Row>
            </Container>
        </Layout>
    );
};

export default MyComponent;
