import React from 'react'
import styles from './ChatbotDirectLink.module.less'
import {faCloud} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'


class ChatbotDirectLink extends React.Component {

    componentDidMount() {
        if (this.props.location.pathname.split('/')[2]) {
            const script = document.createElement("script");
            script.src = "http://localhost:9000/dist/chatbot.js";
            script.async = true;
            script.defer = true;
            script.setAttribute('data-directLink', '');
            script.setAttribute('data-name', 'tsb-widget');
            script.setAttribute('data-id', this.props.location.pathname.split('/')[2]);
            script.setAttribute('data-circle', '#9254de');
            script.setAttribute('dev', '');
            document.body.appendChild(script);
        }
    }

    render() {
        return (
            <div style={{height: '100%'}}>
                <div className={styles.Navbar}>
                    <div>
                        <FontAwesomeIcon size="2x" icon={faCloud} style={{color: '#9254de'}}/>
                        <div style={{
                            lineHeight: '40px',
                            marginLeft: 18,
                            color: "#9254de"
                        }}>TheSearchBase
                        </div>
                    </div>
                </div>
                <div id="directlink" className={styles.Wrapper}></div>
            </div>
        )
    }
}

export default ChatbotDirectLink;
