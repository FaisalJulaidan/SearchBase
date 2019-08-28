import React, {Component} from 'react';
import styles from './nav-item.module.css'
import PropTypes from 'prop-types';

class NavItem extends Component {

    state = {
        title: this.props.title
    };

    render() {
        return (
            <span onClick={this.props.onClick} className={styles.link}>{this.state.title}
                <svg className={styles.arrow} viewBox="0 0 400 1000" preserveAspectRatio="none">
                    <g>
                        <path className="arrow-exterior" stroke="black" fill="#DDEAEF"
                              d="M 100 0 L 400 500 L 100 1000 L 0 1000 L 300 500 L 0 0 L 100 0"/>
                        <path className="arrow-interior" stroke="black" fill="#4AA2C4"
                              d="M 0 0 L 300 500 L 0 1000 L 0 900 L 0 500 L 0 0 L 0 0"/>
                    </g>
                </svg>
            </span>
        );
    }
}

NavItem.propTypes = {
    id: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired
};

export default NavItem;
