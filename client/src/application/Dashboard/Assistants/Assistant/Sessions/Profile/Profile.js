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
            let values = this.props.session.Data.keywordsByDataType[dataType.name];
            let inputs = [];
            if(values){
                values.forEach(input => {
                    if (input === '&FILE_UPLOAD&'){
                        this.counter += 1;
                        inputs.push(this.createDownloadFileBtn(this.counter))
                    } else {
                        inputs.push(<p>{input} </p>)
                    }
                });
            }
            return (
                    <React.Fragment>
                        {inputs.map((input) => input)}
                    </React.Fragment>
                )
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