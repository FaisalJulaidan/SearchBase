import React, {Component} from 'react';
import {connect} from 'react-redux';
import {store} from "store/store";

import {Button, Select, Form, Divider, Row, Col} from "antd";
import {assistantActions, marketplaceActions, autoPilotActions} from "store/actions";
import {history} from "helpers";

const Option = Select.Option;


class Connections extends Component {

    state = {
        selectedCRM: undefined,
        selectedAutoPilot: undefined,
        selectedCalendar: undefined,

        defaultSelectedCRM: undefined,
        defaultSelectedAutoPilot: undefined,
        defaultSelectedCalendar: undefined
    };

    componentWillMount() {
        if (!this.props.autoPilotsList.length) this.props.dispatch(autoPilotActions.fetchAutoPilots());
        this.props.dispatch(marketplaceActions.fetchMarketplace());
    }

    componentWillReceiveProps(nextProps, nextContext) {
        const {assistant, marketplaceItems, autoPilotsList} = nextProps;

        this.setState({
            defaultSelectedCRM: marketplaceItems?.crms?.find(crm => crm.ID === assistant.CRMID),
            defaultSelectedCalendar: marketplaceItems?.calendars?.find(calendar => calendar.ID === assistant.CalendarID),
            defaultSelectedAutoPilot: autoPilotsList.find(ap => ap.ID === assistant.AutoPilotID)
        })
    }

    // CRM
    handleConnectCRM = () => {
        this.props.dispatch(assistantActions.connectToCRM(this.state.selectedCRM.ID, this.props.assistant.ID))
    };

    handleDisconnectCRM = () => {
        this.props.dispatch(assistantActions.disconnectFromCRM(this.props.assistant.ID))
    };


    // Calendar
    handleConnectCalendar = () => {
        this.props.dispatch(assistantActions.connectToCalendar(this.state.selectedCalendar.ID, this.props.assistant.ID))
    };

    handleDisconnectCalendar = () => {
        this.props.dispatch(assistantActions.disconnectFromCalendar(this.props.assistant.ID))
    };


    // Auto Pilot
    handleConnectAutoPilot = () => {
        this.props.dispatch(assistantActions.connectToAutoPilot(this.state.selectedAutoPilot.ID, this.props.assistant.ID))
    };

    handleDisconnectAutoPilot = () => {
        this.props.dispatch(assistantActions.disconnectFromAutoPilot(this.props.assistant.ID))
    };


    render() {
        const {marketplaceItems, autoPilotsList} = this.props;
        const {defaultSelectedCRM, selectedCRM, defaultSelectedCalendar, selectedCalendar, defaultSelectedAutoPilot, selectedAutoPilot} = this.state;
        console.log(defaultSelectedAutoPilot)
        return (
            <>

                <h2> Auto Pilot Connection</h2>
                <div>
                    <Select
                        style={{ width: 500, marginBottom: 10 }}
                        placeholder="Select an Auto Pilot to be connected to this assistant"
                        onChange={(autoPilotID) => this.setState({selectedAutoPilot: autoPilotsList.find(ap => ap.ID === autoPilotID)})}
                        value={selectedAutoPilot ? selectedAutoPilot?.ID : (defaultSelectedAutoPilot?.ID || undefined) }
                    >
                        {autoPilotsList.map((ap, i) => {
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


                <br/>
                <Divider/>
                <h2> CRM Connection:</h2>
                <div>
                    <Select
                        style={{ width: 500, marginBottom: 10 }}
                        placeholder="Select a CRM to be connected to this assistant"
                        onChange={(CRMID) => this.setState({selectedCRM: marketplaceItems?.crms?.find(crm => crm.ID === CRMID)})}
                        value={selectedCRM ? selectedCRM?.ID : (defaultSelectedCRM?.ID || undefined) }
                    >
                        {marketplaceItems?.crms?.map((crm, i) => {
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
                <h2> Calendar Connection (Coming soon)</h2>
                <div>
                    <Select disabled
                        style={{ width: 500, marginBottom: 10 }}
                        placeholder="Select a Calendar to be connected to this assistant"
                        onChange={(calendarID) => this.setState({selectedCalendar: marketplaceItems?.calendars?.find(calendar => calendar.ID === calendarID)})}
                        value={selectedCalendar ? selectedCalendar?.ID : (defaultSelectedCalendar?.ID || undefined) }
                    >
                        {marketplaceItems?.calendars?.map((calendar, i) => {
                            return <Option key={i} value={calendar.ID}>{calendar.Type}</Option>
                        })}
                    </Select>
                </div>
                <div>
                    <Button
                        type={'primary'}
                        onClick={this.handleConnectCalendar}
                        disabled={!(selectedCalendar && selectedCalendar?.ID !== defaultSelectedCalendar?.ID)}
                    >
                        Connect
                    </Button>
                    <Button type={'danger'}
                            onClick={this.handleDisconnectCalendar}
                            disabled={!defaultSelectedCalendar}
                    >
                        {!defaultSelectedCalendar ? "Disconnect" : `Disconnect from ${defaultSelectedCalendar.Type}`}
                    </Button>
                </div>
            </>
        );
    }
}

function mapStateToProps(state) {
    return {
        marketplaceItems: state.marketplace.marketplaceItems,
        autoPilotsList: state.autoPilot.autoPilotsList,
    };
}

export default connect(mapStateToProps)(Form.create()(Connections));
