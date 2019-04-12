import React from 'react';
import CRMModal from './CRMModal/CRMModal'
import {assistantActions} from "store/actions";
import {connect} from 'react-redux';

import {Modal} from 'antd';

const confirm = Modal.confirm;

class CRM extends React.Component {

    state = {};

    componentDidMount() {
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.connectCRMSuccessMsg && this.props.visible)
            this.props.hideModal()
    }

    handleConnect = (CRM) => {
        // dispatch redux action
        this.props.dispatch(assistantActions.connectCRM(CRM, this.props.assistant));
    };

    handleTest = (CRM) => {
        // dispatch redux action
        this.props.dispatch(assistantActions.testCRM(CRM, this.props.assistant));
    };

    handleDisconnect = (CRM) => {
        // dispatch redux action
        confirm({
            title: `Disconnect from ${CRM.type}`,
            content: <p>Chatbot conversations will no longer be synced with {CRM.type} account</p>,
            onOk: () => {
                this.props.dispatch(assistantActions.disconnectCRM(CRM, this.props.assistant));
            }
        });

    };

    render = () => <CRMModal assistant={this.props.assistant}
                             visible={this.props.visible}
                             handleConnect={this.handleConnect}
                             handleTest={this.handleTest}
                             handleCancel={this.props.hideModal}
                             handleDisconnect={this.handleDisconnect}
                             isTestFaild={this.props.testCRMErrorMsg}/>
}

function mapStateToProps(state) {
    return {
        connectCRMSuccessMsg: state.assistant.connectCRMSuccessMsg,
        testCRMErrorMsg: state.assistant.testCRMErrorMsg
    };
}

export default connect(mapStateToProps)(CRM);
