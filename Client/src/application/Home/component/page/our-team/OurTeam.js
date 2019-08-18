import React from 'react';
import styles from './our-team.module.css';
import {Col, Container, Row} from "react-bootstrap";
import HeroLayout from "../../../hoc/hero-layout/HeroLayout";
import teamJson from './team.json';
import MemberCard from "./memeber-card/MemberCard";
import Layout from "../../../hoc/layout/Layout";
import {WEBSITE_TITLE} from '../../../../../constants/config';

const OurTeam = () => {

    document.title = "Our Team | " + WEBSITE_TITLE;

    let team = teamJson.map((member, i) => {
        return (
            <Col key={i} className={styles.card_col} xs={12} sm={6} md={4} lg={3}>
                <MemberCard key={i} img={member.img}
                            name={member.name}
                            title={member.title}
                            desc={member.desc}
                            linkedin={member.linkedin}
                            facebook={member.facebook}
                            twitter={member.twitter}
                            github={member.github}
                />
            </Col>
        );
    });

    return (
        <Layout>
            <HeroLayout title="Our Team" subtitle="Talented people from all around the world.">
                <Container className={styles.container}>
                    <Row className={styles.row}>
                        <Col>
                            <h1>Multiple countries, several timezones and one family</h1>
                            <hr/>
                        </Col>
                    </Row>
                    <Row>
                        {team}
                    </Row>
                </Container>
            </HeroLayout>
        </Layout>
    );
};

export default OurTeam;
