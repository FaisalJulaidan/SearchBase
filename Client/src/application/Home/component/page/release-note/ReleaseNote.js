import React from 'react';
import styles from './release-note.module.css';
import changelog from './changelog';
import ReleaseNoteItem from "./release-note-item/ReleaseNoteItem";
import {Col, Container, Row} from "react-bootstrap";
import Layout from "../../../hoc/layout/Layout";
import {WEBSITE_TITLE} from '../../../../../constants/config';

const ReleaseNote = () => {

    document.title = "Release Notes | " + WEBSITE_TITLE;

    let releaseNoteItems = changelog.map((item, key) => {
        return (
            <ReleaseNoteItem key={key} id={key}
                             version={item.version}
                             tag={item.tag}
                             date={item.date}
                             notes={item.notes}/>
        );
    });

    return (
        <Layout>
            <div>
                <div className={styles.background}>
                    <Container className={styles.text_wrapper}>
                        <Row>
                            <Col md={{offset: 1, span: 2}}>
                                <h1 className={styles.title}>Release notes</h1>
                            </Col>
                        </Row>
                    </Container>

                </div>
                <div className={styles.content}>
                    {releaseNoteItems}
                </div>
            </div>
        </Layout>
    );
};

export default ReleaseNote;
