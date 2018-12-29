import React, {Component} from 'react';
import {Button, message, Skeleton} from 'antd';
import {connect} from 'react-redux';

import "./Assistants.less"
import styles from "./Assistants.module.less"
import Assistant from "./Assistant/Assistant"

import {assistantActions} from "../../../store/actions/assistant.actions";
import NewAssistantModal from "./NewAssistantModal/NewAssistantModal";


class Assistants extends Component {
    state = {
        visible: false,
    };

    componentDidUpdate(prevProps) {
        // Show feedback for settings update
        if (Boolean(this.props.successSettings) && Boolean(prevProps.successSettings) !== Boolean(this.props.successSettings))
            message.success(this.props.successSettings);

        if (Boolean(this.props.errorSettings) && Boolean(prevProps.errorSettings) !== Boolean(this.props.errorSettings))
            message.error(this.props.errorSettings);
    }


    componentDidMount() {
        this.props.dispatch(assistantActions.fetchAssistants());
    }


    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    hideModal = () => {
        this.setState({
            visible: false,
        });
    };


    render() {
        return (
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>Assistants List</h3>
                            <p>Here you can see all assistants created by you</p>
                        </div>
                        <div>
                            <Button className={styles.Panel_Header_Button} type="primary" icon="plus"
                                    onClick={this.showModal}>
                                Add Assistant
                            </Button>
                        </div>

                    </div>


                    <div className={styles.Panel_Body}>
                        <div className={styles.AssistantsList}>
                            {
                                this.props.assistantList[0] ?
                                    (
                                        this.props.assistantList.map((assistant, i) => <Assistant assistant={assistant}
                                                                                                  key={i}
                                                                                                  index={i}
                                                                                                  isLoading={this.props.isLoading}
                                        />)
                                    )
                                    : <Skeleton active/>
                            }
                        </div>
                    </div>

                </div>


                <NewAssistantModal visible={this.state.visible}
                                   hideModal={this.hideModal}/>

            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        assistantList: state.assistant.assistantList,
        isLoading: state.assistant.isLoading,
        successSettings: state.settings.successMsg,
        errorSettings: state.settings.errorMsg,
    };
}

export default connect(mapStateToProps)(Assistants);
