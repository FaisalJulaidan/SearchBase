import React from 'react';
import PropTypes from 'prop-types';
import styles from "./AuroraCard.module.less"

class AuroraCard extends React.Component {
    render() {
        return (
            <button
                className={[styles.SelectButton, styles.Unbuttonized, this.props.selected ? styles.Selected : ''].join(' ')}
                onClick={this.props.onClick}>
                <div className={styles.Head}>
                    <div className={styles.Price}>
                        <img src={this.props.selected ? this.props.selectImage : this.props.image}
                             alt="Head image"
                             width={100}/>

                        <br/>

                        <b>{this.props.title}</b>
                    </div>
                </div>

                <div className={styles.Details}>
                    {this.props.desc}
                </div>
            </button>
        );
    }
}

AuroraCard.propTypes = {
    title: PropTypes.string,
    selected: PropTypes.bool,
    image: PropTypes.string,
    desc: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.element
    ])
};
export default AuroraCard
