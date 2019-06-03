import React from 'react';
import CRMModal from './CRMModal/CRMModal'
import {connect} from 'react-redux';
import {assistantActions} from "store/actions";


class CRM extends React.Component {
    handleSave = CRMID => {
        this.props.hideUploadModal();
        if (CRMID)
            this.props.dispatch(assistantActions.selectAssistantCRM(CRMID, this.props.assistant.ID));
    };

    handleReset = () => {
        this.props.hideUploadModal();
        this.props.dispatch(assistantActions.resetAssistantCRM(this.props.assistant.ID));
    };

    render = () => <CRMModal assistant={this.props.assistant}
                             visible={this.props.visible}
                             handleCancel={this.props.hideUploadModal}
                             handleSave={this.handleSave}
                             handleReset={this.handleReset}
                             CRMsList={this.props.CRMsList}/>
}

export default connect()(CRM);
