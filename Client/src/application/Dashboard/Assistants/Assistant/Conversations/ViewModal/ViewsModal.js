import React, {Component} from 'react';
import {Button, Col, Icon, Modal, Progress, Row, Tabs, Typography} from "antd";
import {destroyMessage, errorMessage, http, loadingMessage, successMessage} from "helpers";
import Profile from '../Profile/Profile'
import Conversation from '../Conversation/Conversation'
import SelectedSolutions from "../SelectedSolutions/SelectedSolutions";
import CRMResponse from "../CRMResponse/CRMResponse";
import styles from "./ViewModal.module.less";

const {Text} = Typography;

const TabPane = Tabs.TabPane;


class ViewsModal extends Component {

    state = {
        isDownloadingFile: false
    };

    constructor(props) {
        super(props);
        this.handleKeyPress = this.handleKeyPress.bind(this);
        console.log(this.props.conversation)
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

    downloadFileHandler = (fileKey) => {
        // Get file name by index
        let file = this.props.conversation.StoredFile.StoredFileInfo.find(sf => sf.FilePath === fileKey);
        if (!file){
            errorMessage("File doesn't exist!");
            return;
        }

        loadingMessage("Downloading file...", 0);
        this.setState({isDownloadingFile: true});
        const conversationID = this.props.conversation.ID
        // Get the pre singed generated url to download from DigitalOcean
        http.get(`/assistant/${this.props.assistant.ID}/conversation/${conversationID}/${file.FilePath}`)
            .then((response) => {
                window.open(response.data.data.url);
                this.setState({isDownloadingFile: false});
                destroyMessage()
            }).catch(error => {
                errorMessage("File is corrupted!");
                this.setState({isDownloadingFile: false});
            });

    };


    render() {
        const {conversation, flowOptions, updateStatus, isUpdatingStatus, buildStatusBadge} = this.props;
        const userType = conversation ? conversation.UserType : 'Unknown';

        return (
            <Modal
                width={900}
                title={
                    <h3>
                        {buildStatusBadge(conversation?.ApplicationStatus, false)}
                        {conversation?.UserType === "Unknown" ? "Conversation" : conversation?.UserType} Details
                        <span>
                            <Text type="secondary"> #{conversation?.ID}</Text>
                        </span>
                    </h3>}
                destroyOnClose={true}
                visible={this.props.visible}
                onCancel={this.props.closeViewModal}
                onOk={this.props.closeViewModal}
                footer={[
                    <Button key="Delete" onClick={() => this.props.deleteConversation(conversation)}
                            type={'danger'}>Delete</Button>,
                    <Button key="Cancel" onClick={this.props.closeViewModal}>OK</Button>,
                ]}>


                <Row type={'flex'} justify={'center'} style={{marginBottom: '20px'}}>
                    <h4 style={{marginRight: 5}}>Score</h4>

                    <Progress percent={conversation?.Score * 100} size="small" style={{width: '50%'}}
                              status={conversation?.Score < 0.1 ? "exception" : "active"}/>
                </Row>
                <Row type={'flex'} justify={'center'} style={{marginBottom: '20px'}}>
                    <Button className={styles.StatusChangeBtn}
                            type={conversation?.Status === "Rejected" ? "link" : "default"}
                            disabled={isUpdatingStatus}
                            onClick={() => updateStatus("Rejected", conversation)}>
                        <Icon type="close-circle" theme="filled"
                              style={{color: "red", fontSize: "18px"}} />
                    </Button>

                    <Button className={styles.StatusChangeBtn}
                            type={conversation?.Status === "Pending" ? "link" : "default"}
                            style={{color: "#faad14", fontSize: "18px"}}
                            disabled={isUpdatingStatus}
                            onClick={() => updateStatus("Pending", conversation)} >
                        <Icon type="clock-circle"/>
                    </Button>

                    <Button className={styles.StatusChangeBtn}
                            type={conversation?.Status === "Accepted" ? "link" : "default"}
                            disabled={isUpdatingStatus}
                            onClick={() => updateStatus("Accepted", conversation)} >
                        <Icon type="check-circle" theme="filled"
                              style={{color: "#52c41a", fontSize: "18px"}} />
                    </Button>
                </Row>


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

                    <TabPane tab={"Profile"} key={"2"}>
                        <Profile conversation={conversation} downloadFile={this.downloadFileHandler}
                                 dataTypes={flowOptions?.dataTypes}
                                 isDownloadingFile={this.state.isDownloadingFile}/>
                    </TabPane>

                    <TabPane tab={"Selected Solutions (Candidates, Jobs)"} key={"3"}>
                        <SelectedSolutions solutions={conversation?.Data?.selectedSolutions}/>
                    </TabPane>

                    <TabPane tab={"CRM Status"} key={"4"}>
                        <CRMResponse conversation={conversation}/>
                    </TabPane>

                </Tabs>
            </Modal>
        );
    }
}

export default ViewsModal;
