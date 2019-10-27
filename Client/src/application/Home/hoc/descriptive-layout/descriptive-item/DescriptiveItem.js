import React from 'react';
import styles from "./descriptive-item.module.css";
import PropTypes from "prop-types";
import Table from "./table/Table";
import Linkify from 'react-linkify';

class DescriptiveItem extends React.Component {
    state = {
        headline: this.props.headline,
        title: this.props.title,
        subtitle: this.props.subtitle,
        items: this.props.items || [],
        texts: this.props.texts || [],
        _table: this.props._table
    };

    componentDecorator = (href, text, key) => (
        <a href={href} key={key} target="_blank">
            {text}
        </a>
    );

    render() {

        let items = this.state.items.map((item, i) => {
            return (
                <li key={i}>{item}</li>
            )
        });

        let texts = this.state.texts.map((text, i) => {
            return (
                <p key={i} className={styles.text}>{text}</p>
            )
        });

        let table;
        if ((typeof this.state._table != "undefined")) {
            table = <Table head={this.state._table.head} body={this.state._table.body}/>
        }


        return (
            <Linkify componentDecorator={this.componentDecorator}>
                <div className={styles.item_wrapper}>
                    <br/>
                    <h2 style={{display: (typeof this.state.headline != "undefined") ? 'block' : 'none'}}
                        className={styles.headline}>{this.state.headline}</h2>
                    <h5 className={styles.title}>{this.state.title}</h5>
                    <p>{this.state.subtitle}</p>
                    <ul style={{display: (this.state.items.length !== 0) ? 'block' : 'none'}}
                        className={styles.items}>
                        {items}
                    </ul>
                    {texts}
                    {table}
                </div>
            </Linkify>
        )
    }
}

DescriptiveItem.propTypes = {
    headline: PropTypes.string,
    title: PropTypes.string,
    subtitle: PropTypes.string,
    items: PropTypes.arrayOf(PropTypes.string),
    texts: PropTypes.arrayOf(PropTypes.string),
    _table: PropTypes.shape({
        head: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.shape({
            text: PropTypes.string,
            items: PropTypes.arrayOf(PropTypes.string)
        }))),
        body: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.shape({
            text: PropTypes.string,
            items: PropTypes.arrayOf(PropTypes.string)
        })))
    }),
};

export default DescriptiveItem;
