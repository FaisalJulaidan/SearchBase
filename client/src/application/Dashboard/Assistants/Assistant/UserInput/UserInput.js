import React from 'react';
import styles from "./UserInput.module.less"
import Header from "../../../../../components/Header/Header";
import {chatbotSessionsActions} from "../../../../../store/actions";
import connect from "react-redux/es/connect/connect";
import Sessions from "./Sessions/Sessions";


class UserInput extends React.Component {

    componentDidMount() {
        const {assistant} = this.props.location.state;
        this.props.dispatch(chatbotSessionsActions.fetchChatbotSessions(assistant.ID))
    }

    clearAllChatbotSessions = () => {
        const {assistant} = this.props.location.state;
        this.props.dispatch(chatbotSessionsActions.clearAllChatbotSessions(assistant.ID))
    };

    render() {
        const {assistant} = this.props.location.state;
        console.log(this.props.chatbotSessions);
        return (

            <div style={{height: '100%'}}>
                <Header display={assistant.Name}/>

                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>{assistant.Name}: User Inputs</h3>
                            <p>Here you can find all the responses to your chatbot</p>
                        </div>
                    </div>

                    <div className={styles.Panel_Body}>
                        <Sessions sessions={this.props.chatbotSessions}
                                  isLoading={this.props.isLoading}
                                  isClearingAll={this.props.isClearingAll}
                                  clearAllChatbotSessions={this.clearAllChatbotSessions}
                                  assistant/>
                    </div>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state =>  {
    const {chatbotSessions} = state;
    return {
        chatbotSessions: chatbotSessions.chatbotSessions,
        isLoading: chatbotSessions.isLoading,
        errorMsg: chatbotSessions.errorMsg,

        isClearingAll: chatbotSessions.isClearingAll
    };
};


export default connect(mapStateToProps)(UserInput);