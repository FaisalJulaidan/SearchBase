import React, {Component} from 'react';
import {Button, Table, Tag, Icon} from "antd";


class Conversation extends Component {

    emailUser = email => {
        window.location.href = "mailto:"+email;
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
                return (<Button
                    disabled={this.props.isDownloadingFile}
                    hreftype="primary" file-path-index={record.fileName} icon="download" size="small"
                    onClick={(e) => {this.props.downloadFile(e.target.getAttribute('file-path-index'))}}>
                    Download File
                </Button>);
            }
            else if (record.dataType.includes("Email")){
                return (<p>
                   {record.input} <Icon type="mail" onClick={()=>{this.emailUser(record.input)}}/>
               </p>);
            }
            else {
               return (<p>
                   {record.input}
               </p>);
            }
        },
    },{
        title: 'Data Type',
        key: 'DataType',
        render: (text, record, index) => (<Tag key={record.UserType}>{record.dataType}</Tag>),
    }];


    render() {
        const {conversation} = this.props;
        return (
            <Table columns={this.columns}
                   dataSource={conversation.Data.collectedData}
                   size='middle'
                   pagination={false}
            />
        );
    }
}

export default Conversation;