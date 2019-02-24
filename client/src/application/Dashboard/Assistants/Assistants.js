import React, {Component} from 'react';
import {Button, Skeleton, Modal} from 'antd';
import {connect} from 'react-redux';

import styles from "./Assistants.module.less"
import Assistant from "./Assistant/Assistant"

import {assistantActions} from "../../../store/actions/assistant.actions";
import NewAssistantModal from "./Modals/NewAssistantModal";
const confirm = Modal.confirm;

class Assistants extends Component {
    state = {
        visible: false,
    };


    componentDidMount() {
        this.props.dispatch(assistantActions.fetchAssistants());
    }


    showModal = () => this.setState({visible: true});
    hideModal = () => this.setState({visible: false});
    activeHandler = (checked, assistantID) => {
        if(!checked){
            confirm({
                title: `Deactivate assistant`,
                content: <p>Are you sure you want to deactivate this assistant</p>,
                onOk: () => {
                    this.props.dispatch(assistantActions.changeAssistantStatus(assistantID, checked))
                }
            });
            return;
        }
        this.props.dispatch(assistantActions.changeAssistantStatus(assistantID, checked))
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
                                                                                                  isStatusChanging={this.props.isStatusChanging}
                                                                                                  activeHandler={this.activeHandler}
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
        registerList: state.assistant.registerList,
        isLoading: state.assistant.isLoading,
        isStatusChanging: state.assistant.isStatusChanging,
    };
}

export default connect(mapStateToProps)(Assistants);
