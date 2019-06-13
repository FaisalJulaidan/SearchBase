import React from 'react'
import {connect} from 'react-redux';
import styles from "./AutoPilots.module.less";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Icon, Typography} from 'antd';
import CreateNewBox from "components/CreateNewBox/CreateNewBox";
import ViewBox from "components/ViewBox/ViewBox";
import {AutoPilotIcon} from "components/SVGs";
import NewAutoPilotModal from './NewAutoPilotModal/NewAutoPilotModal'
import {autoPilotActions} from "store/actions";
import 'types/TimeSlots_Types'
import {history} from "helpers";

const {Title, Paragraph, Text} = Typography;

class AutoPilots extends React.Component {
    state = {visible: false};

    componentDidMount() {
        this.props.dispatch(autoPilotActions.fetchAutoPilots())
    }

    showModal = () => this.setState({visible: true});
    closeModal = () => this.setState({visible: false,});

    render() {
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <Title className={styles.Title}>
                            <Icon type="interation"/> Auto Pilots
                        </Title>
                        <Paragraph type="secondary">
                            Automate your assistants using auto pilots
                        </Paragraph>
                    </div>

                    <div className={styles.Body}>
                        <CreateNewBox text={'Add Auto Pilot'} onClick={this.showModal}/>
                        {
                            this.props.autoPilotsList.map(
                                (/**@type AutoPilots*/ autoPilot, i) =>
                                    <ViewBox
                                        onClick={() => history.push(`/dashboard/auto_pilots/${autoPilot.ID}`)}
                                        key={i}
                                        title={autoPilot.Name}
                                        text={autoPilot.Description}
                                        icon={<AutoPilotIcon/>}
                                        iconTop={175}
                                        iconRight={15}
                                    />
                            )
                        }
                    </div>
                </NoHeaderPanel>

                <NewAutoPilotModal
                    autoPilotsList={this.props.autoPilotsList}
                    visible={this.state.visible}
                    showModal={this.showModal}
                    closeModal={this.closeModal}
                />
            </>
        )
    }
}

function mapStateToProps(state) {
    return {
        autoPilotsList: state.autoPilot.autoPilotsList
    };
}

export default connect(mapStateToProps)(AutoPilots);

