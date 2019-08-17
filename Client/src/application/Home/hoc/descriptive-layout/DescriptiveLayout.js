import React, {Component} from 'react';
import styles from "./descriptive-layout.module.css";
import Layout from "../layout/Layout";
import {Col, Container, Row} from "react-bootstrap";
import PropTypes from "prop-types";
import DescriptiveItem from "./descriptive-item/DescriptiveItem";

class DescriptiveLayout extends Component {

    state = {
        title: this.props.title,
        items: this.props.items || [],
    };

    render() {

        let items = this.state.items.map((item, i) => {
            return (
                <DescriptiveItem key={i}
                                 headline={item.headline}
                                 title={item.title}
                                 subtitle={item.subtitle}
                                 items={item.items}
                                 texts={item.texts}
                                 _table={item._table}
                />
            )
        });

        return (
            <Layout>
                <Container className={styles.container}>
                    <Row>
                        <Col>
                            <h1 className={styles.headline}>{this.state.title}</h1>
                            {items}
                        </Col>
                    </Row>
                </Container>
            </Layout>
        );
    }
}

DescriptiveLayout.propTypes = {
    title: PropTypes.string,
    items: PropTypes.arrayOf(PropTypes.shape({
        headline: PropTypes.string,
        title: PropTypes.string,
        subtitle: PropTypes.string,
        items: PropTypes.arrayOf(PropTypes.string),
        texts: PropTypes.arrayOf(PropTypes.string),
        _table: PropTypes.shape({
            head: PropTypes.arrayOf(PropTypes.shape({
                text: PropTypes.string,
                items: PropTypes.arrayOf(PropTypes.string)
            })),
            body: PropTypes.arrayOf(PropTypes.shape({
                text: PropTypes.string,
                items: PropTypes.arrayOf(PropTypes.string)
            }))
        }),
    })).isRequired
};

export default DescriptiveLayout;