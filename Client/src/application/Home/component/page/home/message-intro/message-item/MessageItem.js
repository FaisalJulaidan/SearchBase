import React, {Component} from 'react';
import styles from './message-item.module.css'
import PropTypes from 'prop-types';

class MessageItem extends Component {

    render() {
        return (
            <div className={styles.message}>
                <div className={(this.props.mine) ? styles.my_message : styles.your_message}>
                    <p className={styles.text}>
                        {this.props.text}
                    </p>
                </div>
            </div>
        );
    }
}

MessageItem.propTypes = {
    mine: PropTypes.bool.isRequired,
    text: PropTypes.string
};

export default MessageItem;