import React, {Component} from 'react';
import styles from './tooltip-menu.module.css';
import {Link} from "react-router-dom";

class MyComponent extends Component {

    render() {
        return (
            <div{...this.props}>
                <div className={styles.tooltip}>
                    <ul>
                        <li><Link to="/our-team">Our Team</Link></li>
                        <li><Link to="/privacy">Privacy Policy</Link></li>
                        <li><Link to="/terms">Terms & Conditions</Link></li>
                    </ul>
                </div>
            </div>
        );
    }
}

MyComponent.propTypes = {};

export default MyComponent;
