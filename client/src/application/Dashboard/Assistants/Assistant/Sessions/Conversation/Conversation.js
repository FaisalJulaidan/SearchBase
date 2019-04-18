import React, {Component} from 'react';
import {Button, Table, Tag} from "antd";


class Conversation extends Component {

    counter = -1; // this is important for specifying what is the file name's index

    componentWillReceiveProps(nextProps, nextContext) {
        if(nextProps.session !== this.props.session){
            this.counter = -1;
        }
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
                return (<Button hreftype="primary" file-path-index={this.counter} icon="download" size="small"
                                onClick={(e) => {this.props.downloadFile(e.target.getAttribute('file-path-index'))}}>
                    Download File
                </Button>);
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