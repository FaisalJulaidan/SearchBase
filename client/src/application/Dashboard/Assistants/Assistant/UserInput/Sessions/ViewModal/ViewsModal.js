import React, {Component} from 'react';
import {Button, Modal, Table, Tabs} from "antd";
import {http, alertError} from '../../../../../../../helpers';
import saveAs from 'file-saver';
import Profile from '../Profile/Profile'
import Conversation from '../Conversation/Conversation'

const TabPane = Tabs.TabPane;


class ViewsModal extends Component {

    counter = -1;
    state = {
        fileNames: []
    };

    columns = [{
        title: 'Question',
        key: 'questionText',
        render: (text, record, index) => (<p>{record.questionText}</p>),
    }, {
        title: 'Input',
        key: 'input',
        render: (text, record, index) => {

            if (record.input === '&FILE_UPLOAD&') {
                this.counter+=1;
                return (<Button hreftype="primary" data-index={this.counter} icon="download" size="small"
                                onClick={(e) => {this.downloadFile(e)}}>
                    Download File
                </Button>);
            }

            else {
               return (<p>
                   {record.input}
               </p>);
            }
        },
    }];

    componentWillReceiveProps(nextProps, nextContext) {
        if(nextProps.record && nextProps.record.FilePath){
            this.setState({fileNames: nextProps.record.FilePath.split(',')})
        }
    }

    downloadFile = (e) => {
        // Get file name by index. indexes stored in each button corresponds to filenames stored in the state
        const fileName = this.state.fileNames[e.target.getAttribute('data-index')];
        if (!fileName){
            alertError("File Error", "Sorry, but file doesn't exist!");
            return;
        }

        http({
            url: `/assistant/${this.props.assistant.ID}/userinput/${fileName}`,
            method: 'GET',
            responseType: 'blob', // important
        }).then((response) => {
            saveAs(new Blob([response.data]), fileName);
        }).catch(error => {
            alertError("File Error", "Sorry, cannot download this file!")
        });
    };

    render() {
        const {session, dataTypes} = this.props;
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
                        <Conversation session={session} />
                    </TabPane>

                    <TabPane tab={`Profile (${userType})`} key={"2"}>
                        <Profile session={session} dataTypes={dataTypes} />
                    </TabPane>

                </Tabs>
            </Modal>
        );
    }
}

export default ViewsModal;