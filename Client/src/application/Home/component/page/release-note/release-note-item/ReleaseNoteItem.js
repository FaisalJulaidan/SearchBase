import React, {Component} from 'react';
import styles from './release-note-item.module.css';
import PropTypes from 'prop-types';
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import {Col} from "react-bootstrap";

class ReleaseNoteItem extends Component {

    state = {
        id: this.props.id,
        version: this.props.version,
        tag: this.props.tag,
        date: this.props.date,
        notes: this.props.notes,
    };

    render() {
        let notes = this.state.notes.map((note, key) => {

            let items = note.items.map((item, i) => {
                return (
                    <li key={i}>{item}</li>
                )
            });

            return (
                <div key={key} className={styles.notes}>
                    <h3 className={styles.title}>{note.title}</h3>
                    <ul className={styles.items}>
                        {items}
                    </ul>
                </div>
            );
        });

        return (
            <div className={styles.item_wrapper}>
                <Container className={styles.container}>
                    <Row>
                        <Col md={{offset:1,span:3}}>
                            <div>
                                <h3 className={styles.version}>{this.props.version}</h3>
                                <p className={styles.tag}>{this.props.tag}</p>
                            </div>
                            <h5 className={styles.latest}
                                style={{display: (this.state.id === 0 ? 'block' : 'none')}}>Latest</h5>
                            <h5 className={styles.date}>{this.props.date}</h5>
                        </Col>
                        <Col md={8}>
                            {notes}
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}

ReleaseNoteItem.propTypes = {
    id: PropTypes.number.isRequired,
    tag: PropTypes.string,
    version: PropTypes.string.isRequired,
    date: PropTypes.string.isRequired,
    notes: PropTypes.array.isRequired
};

export default ReleaseNoteItem;
