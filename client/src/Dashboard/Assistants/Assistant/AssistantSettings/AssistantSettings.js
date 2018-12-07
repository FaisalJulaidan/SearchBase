import React, {Component} from 'react';
import "../Assistant.less"
import connect from "react-redux/es/connect/connect";
import {assistantSettingsActions} from "../../../../store/actions";
import AssistantSettingsModal from "./AssistantSettingsModal/AssistantSettingsModal";

class AssistantSettings extends Component {

    handleSave = (updatedSettings) => {
        this.props.hideModal();
        // dispatch redux action
        this.props.dispatch(assistantSettingsActions.updateAssistantSettingsRequest({
            ID: this.props.assistant.ID,
            updatedSettings: updatedSettings
        }));
    };

    render() {
        return (
            <AssistantSettingsModal assistant={this.props.assistant} visible={this.props.visible}
                                    handleSave={this.handleSave} handleCancel={this.props.hideModal}/>
        )
    }

}

const mapStateToProps = (state) => ({
    isLoading: state.settings.isLoading,
});
export default connect(mapStateToProps)(AssistantSettings);
