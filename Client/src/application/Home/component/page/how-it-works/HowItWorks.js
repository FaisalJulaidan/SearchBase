import React from 'react';
import styles from './how-it-works.module.css';
import descriptiveSectionsJSON from './descriptive-sections.json';
import {WEBSITE_TITLE} from '../../../../../constants/config';
import Layout from "../../../hoc/layout/Layout";
import Steps from "./steps/Steps";
import DescriptiveSection from "./descriptive-section/DescriptiveSection";
import {Col, Container, Row} from "react-bootstrap";

class HowItWorks extends React.Component {

    componentDidMount() {
        document.title = "How it works? | " + WEBSITE_TITLE;
    }

    render() {
        // let features = featuresJson.map((feature, i) => {
        //     return (
        //         <div key={i} className={styles.section}>
        //             <FeatureItem
        //                 title={feature.title}
        //                 subtitle={feature.subtitle}
        //                 text={feature.text}
        //                 img={feature.img}
        //                 textPosition={(i % 2 !== 0)}
        //             />
        //         </div>
        //     )
        // });

        let descriptiveSections = descriptiveSectionsJSON.map((section, i) => {
            return (<DescriptiveSection key={i} id={section.id} intro={section.intro} title={section.title}
                                        texts={section.texts}
                                        image={section.image}
                                        noBackground={(i % 2 !== 0)}/>)
        });

        return (
            <Layout>
                <Container className={styles.container}>
                    <Row>
                        <Col md={{span: 8, offset: 2}} className={styles.col_intro}>
                            <h1>A game changing improvement.</h1>
                            <hr/>
                            <h2>Outsmart, Outperform the competition with Automation.</h2>
                        </Col>
                    </Row>
                </Container>
                <Steps/>
                {/*<Slider/>*/}
                {descriptiveSections}
            </Layout>
        );
    }
}

export default HowItWorks;
