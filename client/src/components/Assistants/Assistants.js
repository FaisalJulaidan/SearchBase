import React, {Component} from 'react';
import {Button, Modal} from 'antd';
import {connect} from 'react-redux';

import "./Assistants.less"
import styles from "./Assistants.module.less"
import Assistant from "../Assistant/Assistant"

import NewRequest from "./NewAssistant/NewRequest"
import {assistantActions} from "../../store/actions/assistant.action";

class Assistants extends Component {
    state = {
        visible: false,
    };

    componentDidMount() {
        this.props.dispatch(assistantActions.fetchAssistants())
    };

    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    handleOk = () => {
        this.setState({
            visible: false,
        });
    };

    handleCancel = () => {
        this.setState({
            visible: false,
        });
    };

    render() {

        return (

            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Header}>
                        <div>
                            <h3>Assistants List</h3>
                            <p>Here you can see all assistants created by you</p>
                        </div>
                        <div>
                            <Button className={styles.AddAssistant} type="primary" icon="plus" onClick={this.showModal}>
                                Add Assistant
                            </Button>
                        </div>

                    </div>


                    <div className={styles.Body}>
                        <div className={styles.AssistantsList}>
                            {this.props.assistantList.map((assistant, i) => <Assistant assistant={assistant} key={i}
                                                                                       index={i}/>)}
                        </div>
                    </div>

                </div>

                <Modal
                    width={800}
                    title="Create New Assistant"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    footer={[
                        <Button key="cancel" onClick={this.handleCancel}>Cancel</Button>,
                        <Button key="submit" type="primary" onClick={this.handleOk}>
                            Submit
                        </Button>,
                    ]}>
                    <NewRequest/>
                </Modal>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        assistantList: state.assistant.assistantList
    };
}

export default connect(mapStateToProps)(Assistants);
