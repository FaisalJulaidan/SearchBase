import React, {Component} from 'react';
import "../Assistant.less"
import SettingsModal from "./SettingsModal/SettingsModal";

class Settings extends Component {


    handleSave = (editedAssistant) => {
        this.props.hideModal();
        console.log(editedAssistant)
        // dispatch redux action
    };

    render = () => <SettingsModal assistant={this.props.assistant} visible={this.props.visible}
                                  handleSave={this.handleSave} handleCancel={this.props.hideModal}/>

}


export default Settings;
