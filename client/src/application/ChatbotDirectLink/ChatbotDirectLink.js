import React from 'react'
import styles from './ChatbotDirectLink.module.less'
import PublicNavbar from "components/PublicNavbar/PublicNavbar";
import axios from "axios";
import {getLink} from "helpers";

class ChatbotDirectLink extends React.Component {

    state = {
        logoPath: null,
        CompanyName: null
    };

    componentDidMount() {
        const assistantID = this.props.location.pathname.split('/')[2];
        if (assistantID) {
            const script = document.createElement("script");
            script.src = getLink("/static/widgets/chatbot.js");
            script.async = true;
            script.defer = true;
            script.setAttribute('data-directLink', '');
            script.setAttribute('data-name', 'tsb-widget');
            script.setAttribute('data-id', assistantID);
            script.setAttribute('data-circle', '#9254de');
            document.body.appendChild(script);

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
            <div style={{height: '100%'}}>
                <PublicNavbar companyLogo={this.state.LogoPath} CompanyName={this.state.CompanyName}/>
                <div id="directlink" className={styles.Wrapper}></div>
            </div>
        )
    }
}

export default ChatbotDirectLink;
