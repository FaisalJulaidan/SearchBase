import React from 'react'
import styles from './Signature.module.css'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faCloud} from '@fortawesome/free-solid-svg-icons'


class Signature extends React.Component {

    render() {

        return (
            <div className={styles.Signature}>
                <p>
                    Chat By
                    <FontAwesomeIcon icon={faCloud} style={{color: '#673AB7', marginLeft: 5}} />
                    <a target="_blank" href="https://thesearchbase.com/">TheSearchBase</a>
                </p>
            </div>
        );
    }

}

export default Signature;
