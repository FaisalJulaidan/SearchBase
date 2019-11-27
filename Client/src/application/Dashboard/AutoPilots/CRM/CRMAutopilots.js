import React from 'react'
import {connect} from 'react-redux';
import styles from "../AutoPilots.module.less";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Icon, Typography, Menu, Modal} from 'antd';
import CreateNewBox from "components/CreateNewBox/CreateNewBox";
import ViewBox from "components/ViewBox/ViewBox";
import LoadingViewBox from "components/LoadingViewBox/LoadingViewBox";
import {AutoPilotIcon} from "components/SVGs";
import NewAutoPilotModal from './Modals/NewCRMAutoPilotModal'
import EditAutoPilotModal from './Modals/EditCRMAutoPilotModal'
import {CRMAutoPilotActions, assistantActions} from "store/actions";
import 'types/TimeSlots_Types'
import {history} from "helpers";

import CRMAutoPilot from './CRMAutopilot'

const {Title, Paragraph} = Typography;

class CRMAutoPilots extends React.Component {

    state = {
        newAutoPilotModalVisible: false,
        editAutoPilotModalVisible: false,
        autoPilotToEdit: null,
        openAutoPilot: null
    };

    componentDidMount() {
        this.props.dispatch(CRMAutoPilotActions.fetchCRMAutoPilots());
        this.props.dispatch(assistantActions.fetchAssistants());
    }

    showNewAutoPilotModal = () => this.setState({newAutoPilotModalVisible: true});
    closeNewAutoPilotModal = () => this.setState({newAutoPilotModalVisible: false,});

    showEditAutoPilotModal = (autoPilot) => this.setState({autoPilotToEdit: autoPilot, editAutoPilotModalVisible: true});
    closeEditAutoPilotModal = () => this.setState({editAutoPilotModalVisible: false});

    addAutoPilot = (values) => {
        this.props.dispatch(CRMAutoPilotActions.addCRMAutoPilot(values));
        this.closeNewAutoPilotModal();
    };

    updateAutoPilot = (autoPilotID, values) => {
        this.props.dispatch(CRMAutoPilotActions.updateCRMAutoPilot(autoPilotID, values));
        this.closeEditAutoPilotModal();
    };

    deleteAutoPilot = (autoPilotID) => {
        Modal.confirm({
            title: `Delete CRM auto pilot confirmation`,
            content: `If you click OK, this auto pilot will be deleted and disconnected from all assistants that are connected to it`,
            onOk: () => {
                console.log(this.props);
                this.props.dispatch(CRMAutoPilotActions.deleteCRMAutoPilot(autoPilotID))
            }
        });
    };

    optionsMenuClickHandler = (e, autoPilot) => {
        if (e.key === 'edit')
            this.showEditAutoPilotModal(autoPilot);
        if (e.key === 'delete')
            this.deleteAutoPilot(autoPilot.ID)
    };

    openAutoPilot = (id) => {
      history.push(`/dashboard/auto_pilots/crm/${id}`) 
      this.setState({openAutoPilot: id}) 
    }


    // it must be an array of Menu.Item. ViewBox expect that in its options Menu
    optionsMenuItems = [
        <Menu.Item style={{padding:10, paddingRight: 30}} key="edit">
            <Icon type="edit" theme="twoTone" twoToneColor="#595959" style={{marginRight: 5}}/>
            Edit
        </Menu.Item>,
        <Menu.Item style={{padding:10, paddingRight: 30}} key="delete">
            <Icon type="delete" theme="twoTone" twoToneColor="#f50808" />
            Delete
        </Menu.Item>
    ];

    render() {
        // let open = this.state.openAutoPilot
        const { openAutoPilot } = this.state
        return (
            <>
                <div className={styles.Body}>
                    <>
                      <CreateNewBox text={'Add CRM Auto Pilot'} onClick={this.showNewAutoPilotModal}/>
                      {
                          this.props.isLoading ? <LoadingViewBox/>
                          :
                          this.props.CRMautoPilotsList.map(
                              (/*@type AutoPilots */ autoPilot, i) =>
                                  <ViewBox
                                      onClick={() => this.openAutoPilot(autoPilot.ID)}
                                      optionsMenuItems={this.optionsMenuItems}
                                      optionsMenuClickHandler={(e)=>this.optionsMenuClickHandler(e, autoPilot)}
                                      key={i}
                                      title={autoPilot.Name}
                                      text={autoPilot.Description}
                                      icon={<AutoPilotIcon/>}
                                      iconTop={175}
                                      iconRight={15}
                                  />
                          )
                      }
                  </> 
                </div>


                <NewAutoPilotModal
                    autoPilotsList={this.props.autoPilotsList}
                    addAutoPilot={this.addAutoPilot}
                    visible={this.state.newAutoPilotModalVisible}
                    showModal={this.showNewAutoPilotModal}
                    closeModal={this.closeNewAutoPilotModal}
                />

                <EditAutoPilotModal
                    autoPilotsList={this.props.autoPilotsList}
                    updateAutoPilot={this.updateAutoPilot}
                    autoPilot={this.state.autoPilotToEdit}
                    visible={this.state.editAutoPilotModalVisible}
                    showModal={this.showEditAutoPilotModal}
                    closeModal={this.closeEditAutoPilotModal}
                />
            </>
        )
    }
}

function mapStateToProps(state) {
    return {
        CRMautoPilotsList: state.CRMAutoPilot.CRMAutoPilotsList,
    };
}

export default connect(mapStateToProps)(CRMAutoPilots);

