import React, {Component} from 'react';
import styles from "./text-item.module.css";
import PropTypes from 'prop-types';

class TextItem extends Component {

    render() {


        //Splitting the first word of the title to make it <b>BOLD</b>
        let firstWordTitle = '';
        let restOfWordsTitle = '';
        if (this.props.title.indexOf(' ') > 0) {
            firstWordTitle = this.props.title.split(' ')[0];
            restOfWordsTitle = this.props.title.substring(this.props.title.indexOf(' '), this.props.title.length);
        } else {
            firstWordTitle = this.props.title;
        }

        return (
            <div className={styles.wrapper}>
                <div className={styles.div_num}>
                    <span>{this.props.number}</span>
                    <hr/>
                </div>
                <h1 className={styles.title}><b>{firstWordTitle}</b>{restOfWordsTitle}</h1>
                <span className={styles.text}>{this.props.text}</span>
            </div>
        );
    }
}

TextItem.propTypes = {
    number: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired
};

export default TextItem;
