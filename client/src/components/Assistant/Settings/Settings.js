import React, {Component} from 'react';
import "../Assistant.less"
import SettingsModal from "./SettingsModal/SettingsModal";
import connect from "react-redux/es/connect/connect";
import {settingsActions} from "../../../store/actions";
import {message} from 'antd';


class Settings extends Component {

    handleSave = (updatedSettings) => {
        this.props.hideModal();
        // dispatch redux action
        this.props.dispatch(settingsActions.updateSettingsRequest({
            ID: this.props.assistant.ID,
            updatedSettings: updatedSettings
        }));
    };

    render() {
        return (
            <SettingsModal assistant={this.props.assistant} visible={this.props.visible}
                           handleSave={this.handleSave} handleCancel={this.props.hideModal}/>
        )
    }

}

const mapStateToProps = (state) => ({
    isLoading: state.settings.isLoading,
});
export default connect(mapStateToProps)(Settings);
