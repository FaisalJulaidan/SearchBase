import React from 'react';
import CRMModal from './CRMModal/CRMModal'
import {assistantActions} from "store/actions";
import {connect} from 'react-redux';

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

    render = () => <CRMModal assistant={this.props.assistant}
                             visible={this.props.visible}
                             handleConnect={this.handleConnect}
                             handleTest={this.handleTest}
                             handleCancel={this.props.hideModal}
                             isTestFaild={this.props.testCRMErrorMsg}/>
}

function mapStateToProps(state) {
    return {
        connectCRMSuccessMsg: state.assistant.connectCRMSuccessMsg,
        testCRMErrorMsg: state.assistant.testCRMErrorMsg
    };
}

export default connect(mapStateToProps)(CRM);
