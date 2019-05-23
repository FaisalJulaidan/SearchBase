import React, {Component} from 'react';
import {Button, Modal, Tabs, Row, Col, Icon, Typography} from "antd";
import {http, alertError, loadingMessage, errorMessage, successMessage} from "helpers";
import saveAs from 'file-saver';
import Profile from '../Profile/Profile'
import Conversation from '../Conversation/Conversation'
import SelectedSolutions from "../SelectedSolutions/SelectedSolutions";
import CRMResponse from "../CRMResponse/CRMResponse";

const {Text} = Typography;

const TabPane = Tabs.TabPane;


class ViewsModal extends Component {

    state = {
        isDownloadingFile: false
    };

    constructor(props) {
        super(props);
        this.handleKeyPress = this.handleKeyPress.bind(this);
    }

    componentDidMount() {
        document.addEventListener('keydown', this.handleKeyPress);
    }

    componentWillUnmount() {
        // you need to unbind the same listener that was binded.
        document.removeEventListener('keydown', this.handleKeyPress, false);
    }

    handleKeyPress = (e) => {
        e.preventDefault();
        if (e.keyCode === 37)// left arrow
            this.props.getBackConversation(this.props.conversation);
        else if (e.keyCode === 39) // right arrow
            this.props.getNextConversation(this.props.conversation);
        else if (e.keyCode === 8 || e.keyCode === 46) // delete or backspace
            this.props.deleteConversation(this.props.conversation)
    };

    downloadFileHandler = (filenameIndex) => {
        // Get file name by index
        let fileName = this.props.conversation.FilePath.split(',')[filenameIndex];


        if (!fileName){
            errorMessage("File doesn't exist!");
            return;
        }

        loadingMessage("Downloading file...", 0);
        this.setState({isDownloadingFile: true});
        http({
            url: `/assistant/${this.props.assistant.ID}/conversations/${fileName}`,
            method: 'GET',
            responseType: 'blob', // important
        }).then((response) => {
            saveAs(new Blob([response.data]), fileName);
            successMessage("File downloaded successfully!");
            this.setState({isDownloadingFile: false});
        }).catch(error => {
            errorMessage("File is corrupted!");
            this.setState({isDownloadingFile: false});
        });

    };


    render() {
        const {conversation, flowOptions} = this.props;
        const userType = conversation ? conversation.UserType : 'Unknown';

        return (
            <Modal
                width={900}
                title={<h3>Conversation Details <span><Text type="secondary">#{conversation?.ID}</Text></span></h3>}
                destroyOnClose={true}
                visible={this.props.visible}
                onCancel={this.props.closeViewModal}
                onOk={this.props.closeViewModal}
                footer={[
                    <Button hidden key="Delete" onClick={() => this.props.deleteConversation(conversation)}
                            type={'danger'}>Delete</Button>,
                    <Button key="Cancel" onClick={this.props.closeViewModal}>OK</Button>,
                ]}>

                <Row type={'flex'} justify={'center'}>
                    <Col span={3}>
                        <Button block onClick={() => this.props.getBackConversation(conversation)}>
                            <Icon type="left"/>Back
                        </Button>
                    </Col>

                    <Col span={18}>
                        <h3 style={{textAlign: 'center'}}>Navigate</h3>
                    </Col>

                    <Col span={3}>
                        <Button block onClick={() => this.props.getNextConversation(conversation)}>
                            Next<Icon type="right"/>
                        </Button>
                    </Col>
                </Row>

                <Tabs defaultActiveKey={"1"}>

                    <TabPane tab={"Conversation"} key={"1"}>
                        <Conversation conversation={conversation}
                                      downloadFile={this.downloadFileHandler}
                                      isDownloadingFile={this.state.isDownloadingFile}/>
                    </TabPane>

                    <TabPane tab={`Profile (${userType})`} key={"2"}>
                        <Profile conversation={conversation} downloadFile={this.downloadFileHandler}
                                 dataTypes={flowOptions?.dataTypes}
                                 isDownloadingFile={this.state.isDownloadingFile}/>
                    </TabPane>

                    <TabPane tab={"Selected Solutions (Candidates, Jobs)"} key={"3"}>
                        <SelectedSolutions solutions={conversation?.Data?.selectedSolutions}/>
                    </TabPane>

                    <TabPane tab={"CRM Status"} key={"4"} disabled={!(conversation?.CRMResponse)}>
                        <CRMResponse conversation={conversation}/>
                    </TabPane>

                </Tabs>
            </Modal>
        );
    }
}

export default ViewsModal;
