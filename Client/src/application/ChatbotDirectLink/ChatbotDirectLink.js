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
            if (process.env.REACT_APP_ENV === 'development')
                s.src = "http://localhost:3001/vendor/js/bundle.js";
            else
                s.src = getLink("/api/widgets/chatbot");
            document.body.appendChild(s);

            axios.get(`/api/assistant/${assistantID}/chatbot`)
                .then(res => {
                    const data = res.data.data;
                    if(data.companyName){
                        document.title = `${data.companyName} Chatbot` 
                    }
                    // if(data.assistant.LogoPath){
                    //     this.setFavicon(data.assistant.LogoPath)
                    // }
                    this.setState({
                        LogoPath: data.assistant.LogoPath,
                        CompanyName: data.CompanyName,
                    });
                })
        }
    }

    setFavicon = (href) => {
      let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
      link.type = 'image/x-icon';
      link.rel = 'shortcut icon';
      link.href = href;
      document.getElementsByTagName('head')[0].appendChild(link);
    }

    render() {
        return (
            <div style={{height: '100%', background: '#F4F6FC'}}>
                <PublicNavbar logoPath={this.state.LogoPath} companyName={this.state.CompanyName}
                              hideOnMobile={true}/>
                <div id={'direct_link_container'} className={styles.Wrapper}/>
            </div>
        )
    }
}

export default ChatbotDirectLink;
