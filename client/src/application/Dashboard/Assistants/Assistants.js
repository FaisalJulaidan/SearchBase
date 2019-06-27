import React, {Component} from 'react';
import {Modal, Typography, Icon, Menu} from 'antd';
import {connect} from 'react-redux';

import styles from "./Assistants.module.less"

import {assistantActions, marketplacesActions} from "store/actions";
import {RobotIcon} from "components/SVGs";
import {history} from "helpers";

import NewAssistantModal from "./Modals/NewAssistantModal";
import EditAssistantModal from "./Modals/EditAssistantModal";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import CreateNewBox from "components/CreateNewBox/CreateNewBox"
import ViewBox from "components/ViewBox/ViewBox";
import LoadingViewBox from "components/LoadingViewBox/LoadingViewBox";


const {Title, Paragraph, Text} = Typography;
const confirm = Modal.confirm;

class Assistants extends Component {
    state = {
        newAssistantModalVisible: false,
        editModalVisible: false,
        assistantToEdit: null
    };

    componentWillMount() {
        this.props.dispatch(assistantActions.fetchAssistants());
    }

    showNewAssistantModal = () => this.setState({newAssistantModalVisible: true});
    hideNewAssistantModal = () => this.setState({newAssistantModalVisible: false});

    showEditModal = (assistant) => this.setState({editModalVisible: true, assistantToEdit: assistant});
    hideEditModal = () => this.setState({editModalVisible: false});

    addAssistant = (values) => {
        this.props.dispatch(assistantActions.addAssistant(values));
        this.hideNewAssistantModal();
    };

    updateAssistant = (assistantID, values) => {
        this.props.dispatch(assistantActions.updateAssistant(assistantID, values));
        this.hideEditModal();
    };

    deleteAssistant = (assistantID) => {
        confirm({
            title: `Delete assistant confirmation`,
            content: `If you click OK, this assistant will be deleted with its content forever`,
            onOk: () => {
                this.props.dispatch(assistantActions.deleteAssistant(assistantID));
            }
        });
    };


    isAssistantNameValid = (name) => {
        console.log(name);
        return !(this.props.assistantList.findIndex(assistant => assistant.Name.toLowerCase() === name.toLowerCase()) >= 0)
    };

    optionsMenuClickHandler = (e, assistant) => {
        if (e.key === 'edit')
            this.showEditModal(assistant);
        if (e.key === 'delete')
            this.deleteAssistant(assistant.ID)
    };

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
        return (
        <>
            <NoHeaderPanel>
                <div className={styles.Header}>
                    <Title className={styles.Title}>
                        <Icon type="robot"/> Assistants
                    </Title>
                    <Paragraph type="secondary">
                        Here you can see all assistants created by you
                    </Paragraph>
                </div>

                <div className={styles.Body}>
                    <CreateNewBox text={'Add Assistant'} onClick={this.showNewAssistantModal}/>
                    {
                        this.props.isLoading ? <LoadingViewBox/>
                        :
                        this.props.assistantList.map(
                            (assistant, i) =>
                                <ViewBox
                                    onClick={() => history.push(`/dashboard/assistants/${assistant.ID}`)}
                                    optionsMenuItems={this.optionsMenuItems}
                                    optionsMenuClickHandler={(e)=>this.optionsMenuClickHandler(e, assistant)}
                                    key={i}
                                    title={assistant.Name}
                                    text={assistant.Description || "No description"}
                                    icon={<RobotIcon/>}
                                    iconWidth={75} iconHeight={75} iconTop={183} iconRight={15}
                                />
                        )
                    }
                </div>
            </NoHeaderPanel>

            <NewAssistantModal visible={this.state.newAssistantModalVisible}
                               addAssistant={this.addAssistant}
                               isAssistantNameValid={this.isAssistantNameValid}
                               hideModal={this.hideNewAssistantModal}/>

            <EditAssistantModal visible={this.state.editModalVisible}
                       assistant={this.state.assistantToEdit}
                       hideModal={this.hideEditModal}
                       isAssistantNameValid={this.isAssistantNameValid}
                       updateAssistant={this.updateAssistant}
            />
        </>
        );
    }
}

function mapStateToProps(state) {
    return {
        assistantList: state.assistant.assistantList,
        options: state.options.options,
        isLoading: state.assistant.isLoading,
    };
}

export default connect(mapStateToProps)(Assistants);
