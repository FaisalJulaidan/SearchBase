import React, {Component} from 'react';
import connect from "react-redux/es/connect/connect";
import {assistantActions} from "store/actions";
import AssistantSettingsModal from "./AssistantSettingsModal/AssistantSettingsModal";
import {Modal} from "antd";

const confirm = Modal.confirm;


class AssistantSettings extends Component {

    handleSave = (updatedSettings) => {
        this.props.hideNewAssistantModal();
        // dispatch redux action
        this.props.dispatch(assistantActions.updateAssistant(this.props.assistant.ID, updatedSettings));
    };

    ////// DELETE GROUP
    handleDelete = (deletedAssistant) => {
        confirm({
            title: `Delete assistant confirmation`,
            content: `If you click OK, this assistant will be deleted with its associated data forever`,
            onOk: () => {
                this.props.dispatch(assistantActions.deleteAssistant(this.props.assistant.ID));
                this.props.hideNewAssistantModal();
            }
        });
    };

    render() {
        return (
            <AssistantSettingsModal assistant={this.props.assistant} visible={this.props.visible}
                                    handleSave={this.handleSave}
                                    handleCancel={this.props.hideNewAssistantModal}
                                    handleDelete={this.handleDelete}
                                    isAssistantNameValid={this.props.isAssistantNameValid}/>
        )
    }

}

const mapStateToProps = (state) => ({
    isLoading: state.assistant.isLoading,
});
export default connect(mapStateToProps)(AssistantSettings);
