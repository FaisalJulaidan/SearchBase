import React, {Component} from 'react';
import {connect} from 'react-redux';
import {store} from "store/store";

import {Button, Select, Form, Divider, Row, Col} from "antd";
import {assistantActions, marketplacesActions} from "store/actions";
import {history} from "helpers";

const Option = Select.Option;


class Connections extends Component {

    state = {
        selectedCRM: undefined,
        selectedAutoPilot: undefined,

        defaultSelectedCRM: undefined,
        defaultSelectedAutoPilot: undefined,
    };

    componentWillReceiveProps(nextProps, nextContext) {
        const {assistant, CRMsList, autoPilotsList} = nextProps;
        this.setState({
            defaultSelectedCRM: CRMsList.find(crm => crm.ID === assistant.CRMID),
            defaultSelectedAutoPilot: autoPilotsList.find(ap => ap.ID === assistant.autoPilotID)
        })
    }

    handleConnectCRM = () => {
        this.props.dispatch(assistantActions.connectAssistantCRM(this.state.selectedCRM.ID, this.props.assistant.ID))
    };

    handleDisconnectCRM = () => {
        this.props.dispatch(assistantActions.disconnectAssistantCRM(this.props.assistant.ID))
    };

    handleConnectAutoPilot = () => {
        this.props.dispatch(assistantActions.connectAutoPilot(this.state.selectedAutoPilot.ID, this.props.assistant.ID))
    };

    handleDisconnectAutoPilot = () => {
        this.props.dispatch(assistantActions.disconnectAutoPilot(this.props.assistant.ID))
    };


    render() {
        const {CRMsList, autoPilotsList} = this.props;
        const {defaultSelectedCRM, selectedCRM, defaultSelectedAutoPilot, selectedAutoPilot} = this.state;
        return (
            <>
                <h2> CRM Connection:</h2>
                <div>
                    <Select
                        style={{ width: 500, marginBottom: 10 }}
                        placeholder="Select a CRM to be connected to this assistant"
                        onChange={(CRMID) => this.setState({selectedCRM: CRMsList.find(crm => crm.ID === CRMID)})}
                        value={selectedCRM ? selectedCRM?.ID : (defaultSelectedCRM?.ID || undefined) }
                    >
                        {this.props.CRMsList.map((crm, i) => {
                            return <Option key={i} value={crm.ID}>{crm.Type}</Option>
                        })}
                    </Select>
                </div>
                <div>
                    <Button
                        type={'primary'}
                        onClick={this.handleConnectCRM}
                        disabled={!(selectedCRM && selectedCRM?.ID !== defaultSelectedCRM?.ID)}
                    >
                        Connect
                    </Button>
                    <Button type={'danger'}
                            onClick={this.handleDisconnectCRM}
                            disabled={!defaultSelectedCRM}
                    >
                        {!defaultSelectedCRM ? "Disconnect" : `Disconnect from ${defaultSelectedCRM.Type}`}
                    </Button>
                </div>


                <br/>
                <Divider/>
                <h2> Auto Pilot Connection:</h2>
                <div>
                    <Select
                        style={{ width: 500, marginBottom: 10 }}
                        placeholder="Select an Auto Pilot to be connected to this assistant"
                        onChange={(autoPilotID) => this.setState({selectedAutoPilot: autoPilotsList.find(ap => ap.ID === autoPilotID)})}
                        value={selectedAutoPilot ? selectedAutoPilot?.ID : (defaultSelectedAutoPilot?.ID || undefined) }
                    >
                        {this.props.autoPilotsList.map((ap, i) => {
                            return <Option key={i} value={ap.ID}>{ap.Name}</Option>
                        })}
                    </Select>
                </div>
                <div>
                    <Button
                        type={'primary'}
                        onClick={this.handleConnectAutoPilot}
                        disabled={!(selectedAutoPilot && selectedAutoPilot?.ID !== defaultSelectedAutoPilot?.ID)}
                    >
                        Connect
                    </Button>
                    <Button type={'danger'}
                            onClick={this.handleDisconnectAutoPilot}
                            disabled={!defaultSelectedAutoPilot}
                    >
                        {!defaultSelectedAutoPilot ? "Disconnect" : `Disconnect from ${defaultSelectedAutoPilot.Name}`}
                    </Button>
                </div>


            </>
        );
    }
}

function mapStateToProps(state) {
    return {};
}

export default connect(mapStateToProps)(Form.create()(Connections));
