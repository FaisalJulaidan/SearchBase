import React from 'react'
import styles from './ChatbotDirectLink.module.less'
import PublicNavbar from "components/PublicNavbar/PublicNavbar";
import axios from "axios";
import {getLink} from 'helpers'

class ChatbotDirectLink extends React.Component {

    state = {
        logoPath: null,
        CompanyName: null
    };

    componentDidMount() {
        const assistantID = this.props.location.pathname.split('/')[2];
        if (assistantID) {
            const script = document.createElement("script");

            // Development
            if (process.env.NODE_ENV === 'development')
                script.src = "http://localhost:3001/vendor/js/bundle.js";
            else {

                script.src = getLink("/static/widgets/vendor/js/main.5a3a2054.js");
                script.async = true;
                script.defer = true;
                script.setAttribute('directLink', '');
                script.setAttribute('data-name', 'tsb-widget');
                script.setAttribute('data-id', assistantID);
                script.setAttribute('data-circle', '#68de41');
                document.body.appendChild(script);

                const link = document.createElement("link");
                link.href = getLink('/static/widgets/vendor/css/main.9fcdf850.css');
                link.type = "text/css";
                link.rel = "stylesheet";
                document.getElementsByTagName("head")[0].appendChild(link);
            }

            axios.get(`/api/assistant/${assistantID}/chatbot`)
                .then(res => {
                    const data = res.data.data;
                    this.setState({
                        LogoPath: data.assistant.LogoPath,
                        CompanyName: data.assistant.CompanyName,
                    });
                })
        }
    }

    render() {
        return (
            <div style={{height: '100%', background: '#F4F6FC'}}>
                <PublicNavbar companyLogo={this.state.LogoPath} CompanyName={this.state.CompanyName}/>
                <div id={'direct_link_container'} className={styles.Wrapper}>
                </div>
            </div>
        )
    }
}

export default ChatbotDirectLink;
