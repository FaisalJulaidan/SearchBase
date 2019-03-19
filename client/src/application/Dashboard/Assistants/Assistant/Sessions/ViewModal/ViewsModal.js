import React, {Component} from 'react';
import {Button, Modal, Table, Tabs} from "antd";
import {http, alertError} from '../../../../../../helpers';
import saveAs from 'file-saver';
import Profile from '../Profile/Profile'
import Conversation from '../Conversation/Conversation'
import SelectedSolutions from "../SelectedSolutions/SelectedSolutions";

const TabPane = Tabs.TabPane;


class ViewsModal extends Component {

    counter = -1;
    state = {
        fileNames: []
    };

    componentWillReceiveProps(nextProps, nextContext) {
        if(nextProps.session && nextProps.session.FilePath){
            this.setState({fileNames: nextProps.session.FilePath.split(',')})
        }
    }

    downloadFileHandler = (filenameIndex) => {
        console.log(filenameIndex);
        // Get file name by index. indexes stored in each button corresponds to filenames stored in the state
        const fileName = this.state.fileNames[filenameIndex];
        if (!fileName){
            alertError("File Error", "Sorry, but file doesn't exist!");
            return;
        }

        http({
            url: `/assistant/${this.props.assistant.ID}/chatbotSessions/${fileName}`,
            method: 'GET',
            responseType: 'blob', // important
        }).then((response) => {
            saveAs(new Blob([response.data]), fileName);
        }).catch(error => {
            alertError("File Error", "Sorry, cannot download this file!")
        });
    };


    render() {
        const {session, flowOptions} = this.props;
        const userType = session ? session.UserType : 'Unknown';

        return (
            <Modal
                width={800}
                title="Session Details"
                destroyOnClose={true}
                visible={this.props.visible}
                onCancel={this.props.closeViewModal}
                onOk={this.props.closeViewModal}
                footer={[
                    <Button key="Cancel" onClick={this.props.closeViewModal}>OK</Button>
                ]}>
                <Tabs defaultActiveKey={"1"}>

                    <TabPane tab={"Conversation"} key={"1"}>
                        <Conversation session={session}
                                      downloadFile={this.downloadFileHandler} />
                    </TabPane>

                    <TabPane tab={`Profile (${userType})`} key={"2"}>
                        <Profile session={session} downloadFile={this.downloadFileHandler}
                                 dataTypes={flowOptions?.dataTypes} />
                    </TabPane>

                    <TabPane tab={"Selected Solutions (Candidates, Jobs)"} key={"3"}>
                        <SelectedSolutions solutions={session?.Data?.selectedSolutions}/>
                    </TabPane>

                </Tabs>
            </Modal>
        );
    }
}

export default ViewsModal;