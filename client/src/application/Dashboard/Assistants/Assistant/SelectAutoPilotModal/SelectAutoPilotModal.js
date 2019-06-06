import React from 'react';
import {connect} from 'react-redux';
import {Button, Icon, Modal, Popconfirm} from "antd";
import {store} from "store/store";
import {assistantActions, autoPilotActions} from "store/actions";
import ViewBox from "components/ViewBox/ViewBox";
import styles from './SelectAutoPilotModal.module.less'
import {AutoPilotIcon} from "components/SVGs";
import 'types/TimeSlots_Types'

class SelectAutoPilotModal extends React.Component {

    state = {};

    componentDidMount() {
        store.dispatch(autoPilotActions.fetchAutoPilots());
    }

    connectAutoPilot = id => store.dispatch(assistantActions.selectAutoPilot(this.props.assistant.ID, id));
    disconnectAutoPilot = id => store.dispatch(assistantActions.disconnectAutoPilot(this.props.assistant.ID, id));

    render = () => (
        <Modal title="Auto Pilot Selection"
               visible={this.props.selectAutoPilotModalVisible}
               width={800}
               destroyOnClose={true}
               onCancel={this.props.hideNewAssistantModal}
               footer={[
                   <Button key="reset" onClick={this.props.hideNewAssistantModal}>Close</Button>,
                   <Popconfirm key="disconnect"
                               title="Are you sure disconnect this assistant?"
                               onConfirm={() => {
                                   this.disconnectAutoPilot();
                                   this.props.hideNewAssistantModal()
                               }}
                               onCancel={this.props.hideNewAssistantModal}
                               okText="Yes"
                               cancelText="No">
                       <Button type={'danger'}>Disconnect All</Button>
                   </Popconfirm>,
               ]}>

            <h3>Click on Auto Pilot to link it with this assistant</h3>
            <p>If nothing shows, navigate to Auto Pilot to create one</p>
            <div className={styles.List}>
                {
                    this.props.autoPilotsList.map(
                        (/**@type AutoPilot*/ autoPilot, i) =>
                            <ViewBox
                                onClick={() => this.connectAutoPilot(autoPilot.ID)}
                                key={i}
                                title={autoPilot.Name}
                                text={autoPilot.Description}
                                icon={<AutoPilotIcon/>}
                                icon2={this.props.assistant.AutoPilotID === autoPilot.ID ?
                                    <Icon type="check-circle" theme="twoTone" twoToneColor="#52c41a"/>
                                    : null}
                                iconTop={175}
                                iconRight={15}
                            />
                    )
                }
            </div>

        </Modal>
    )
}

function mapStateToProps(state) {
    return {
        autoPilotsList: state.autoPilot.autoPilotsList
    };
}

export default connect(mapStateToProps)(SelectAutoPilotModal);
