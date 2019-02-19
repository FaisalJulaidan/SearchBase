import React, {Component} from 'react';
import {Button, Table} from "antd";



class Profile extends Component {

    counter = -1;
    state = {
        fileNames: []
    };

    columns = [{
        title: 'Data Type',
        key: 'dataType',
        render: (text, dataType, index) => {
            return(<p>{dataType.name}</p>)
        },
    }, {
        title: 'Value',
        key: 'input',
        render: (text, dataType, index) => {

            // Find the session with that current dataType in the row from the list of collectedData
            let sessions = this.props.session.Data.collectedData
                .filter((data)=> data.dataType === dataType.name);
            if (sessions.length < 1) return null;

            // If there are more than one inputs of the same dataType then concat them
            let input = "";
            let downloadFilesBtns = [];
            let isFiles = false;

            // If there are multiple records of the same data type
            if (sessions.length > 1){
                sessions.forEach(session => {
                    console.log(session);
                    // Only when file upload do the following
                    if(session.input === '&FILE_UPLOAD&'){
                        this.counter += 1;
                        downloadFilesBtns.push(this.createDownloadFileBtn(this.counter));
                        console.log(downloadFilesBtns);
                        isFiles = true;
                    } else {
                        input += session.input + " | ";
                    }
                });

            // If there is one record of the same data type
            } else {
                if(sessions[0].input === '&FILE_UPLOAD&'){
                    this.counter += 1;
                    input = this.createDownloadFileBtn(this.counter);
                } else {
                    input = sessions[0].input;
                }
            }

            // If there are files to be download
            if (isFiles){
                return (
                    <React.Fragment>
                        {downloadFilesBtns.map((fileBtn) => fileBtn)}
                        | {input}
                    </React.Fragment>
                )
            }

            // If only normal text and no files
            return (<p>{input}</p>);

        }
    }];

    createDownloadFileBtn = (index) => {
        return (<Button key={index} hreftype="primary" file-path-index={index} icon="download"
                        size="small" style={{margin: '0 5px 0 5px'}}
                        onClick={(e) => {this.props.downloadFile(e.target.getAttribute('file-path-index'))}}>
                    Download File
                </Button>);
    };
 
    render() {
        const {session, dataTypes} = this.props;
        console.log(this.state);
        return (
            <Table columns={this.columns}
                   dataSource={dataTypes.filter((type) => type.userTypes.includes(session.UserType))}
                   size='middle'
                   pagination={false}
            />
        );
    }
}

export default Profile;