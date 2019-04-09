import React from 'react';
import CRMModal from './CRMModal/CRMModal'
import {assistantActions} from "store/actions";
import {connect} from 'react-redux';

class CRM extends React.Component {

    state = {};

    componentDidMount() {
    }

    handleConnect = (CRM) => {
        this.props.hideModal();
        // dispatch redux action
        this.props.dispatch(assistantActions.connectCRM(CRM, this.props.assistant));
    };

    render = () => <CRMModal assistant={this.props.assistant}
                             visible={this.props.visible}
                             handleConnect={this.handleConnect}
                             handleCancel={this.props.hideModal}/>

}

export default connect()(CRM);