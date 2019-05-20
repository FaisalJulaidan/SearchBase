import React, {Component} from 'react';
import {Button, Table, Tag, Icon} from "antd";


class Conversation extends Component {

    counter = -1; // this is important for specifying what is the file name's index

    componentWillUpdate(nextProps, nextState, nextContext) {
        this.counter = -1;
    }

    emailUser(email){
        window.location.href = "mailto:"+email;
    }

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
                return (<Button
                    disabled={this.props.isDownloadingFile}
                    hreftype="primary" file-path-index={this.counter} icon="download" size="small"
                    onClick={(e) => {this.props.downloadFile(e.target.getAttribute('file-path-index'))}}>
                    Download File
                </Button>);
            }
            else if (record.dataType.includes("Email")){
                return (<p>
                   {record.input} <Icon type="mail" onClick={()=>{console.log(record.input);this.emailUser(record.input)}}/>
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
        const {session} = this.props;
        return (
            <Table columns={this.columns}
                   dataSource={session.Data.collectedData}
                   size='middle'
                   pagination={false}
            />
        );
    }
}

export default Conversation;