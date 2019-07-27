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
            const s = document.createElement("script");
            s.setAttribute('directLink', '');
            s.setAttribute('data-name', 'tsb-widget');
            s.setAttribute('data-id', assistantID);
            s.setAttribute('data-circle', '#9254de');

            // Development
            if (process.env.NODE_ENV === 'development')
                s.src = "http://localhost:3001/vendor/js/bundle.js";
            else
                s.src = getLink("/api/widgets/chatbot");

            document.body.appendChild(s);

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
                <PublicNavbar companyLogo={this.state.LogoPath} CompanyName={this.state.CompanyName}
                              HideOnMobile={true}/>
                <div id={'direct_link_container'} className={styles.Wrapper}/>
            </div>
        )
    }
}

export default ChatbotDirectLink;
