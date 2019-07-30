import React from 'react';
import './styles/Signature.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloud } from '@fortawesome/free-solid-svg-icons';


class Signature extends React.Component {

    render() {

        return (
            <div className={'Signature'}>
                <p>
                    Chat By
                    <FontAwesomeIcon icon={faCloud} style={{color: '#673AB7', marginLeft: 5}} />
                    <a target="_blank" rel="noopener noreferrer" href="https://thesearchbase.com/">SearchBase</a>
                </p>
            </div>
        );
    }

}

export default Signature;
