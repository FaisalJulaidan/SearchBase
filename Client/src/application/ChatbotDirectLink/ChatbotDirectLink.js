import React from 'react'
import styles from './ChatbotDirectLink.module.less'
import PublicNavbar from "components/PublicNavbar/PublicNavbar";
import axios from "axios";

class ChatbotDirectLink extends React.Component {

    state = {
        logoPath: null,
        CompanyName: null
    };

    componentDidMount() {
        const assistantID = this.props.location.pathname.split('/')[2];
        if (assistantID) {

            const root = document.createElement('div');
            root.id = "TheSearchBase_Chatbot";
            document.body.appendChild(root);


            const script = document.createElement("script");
            // Development
            script.src = "http://localhost:3000/vendor/js/bundle.js";
            // script.src = getLink("/static/widgets/build/vendor/js/main.5a3a2054.js");

            script.async = true;
            script.defer = true;
            script.setAttribute('data-directLink', '');
            script.setAttribute('data-name', 'tsb-widget');
            script.setAttribute('data-id', assistantID);
            script.setAttribute('data-circle', '#9254de');
            document.body.appendChild(script);


            // var link = document.createElement("link");
            // link.href = getLink('/static/widgets/build/vendor/css/main.9fcdf850.css');
            // link.type = "text/css";
            // link.rel = "stylesheet";
            // document.getElementsByTagName("head")[0].appendChild(link);




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
