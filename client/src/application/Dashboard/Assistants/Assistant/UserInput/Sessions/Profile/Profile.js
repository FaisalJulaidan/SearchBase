import React, {Component} from 'react';
import {Button, Table} from "antd";
import {http, alertError} from '../../../../../../../helpers';
import saveAs from 'file-saver';


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
            if (sessions.length > 1){
                sessions.forEach(session => {
                    input += session.input + " | "
                });
            } else {
                input = sessions[0].input;
            }

            // Only when file upload do the following
            if (input === '&FILE_UPLOAD&') {
                this.counter += 1;
                return (<Button hreftype="primary" data-index={this.counter} icon="download" size="small"
                                onClick={(e) => {
                                    this.downloadFile(e)
                                }}>
                    Download File
                </Button>);
            } else {
                return (<p>
                    {input}
                </p>);
            }
        }
    }];

    componentWillReceiveProps(nextProps, nextContext) {
        if(nextProps.session && nextProps.session.FilePath){
            this.setState({fileNames: nextProps.session.FilePath.split(',')})
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