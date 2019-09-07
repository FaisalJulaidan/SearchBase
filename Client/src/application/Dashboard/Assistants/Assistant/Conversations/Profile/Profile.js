import React, {Component} from 'react';
import {Button, Table, Empty} from "antd";



class Profile extends Component {

    counter = -1;

    componentWillReceiveProps(nextProps, nextContext) {
        if(nextProps.conversation !== this.props.conversation){
            this.counter = -1;
        }
    }

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
            let values = this.props.conversation.Data.keywordsByDataType[dataType.name];

            let inputs = [];
            if(values){
                values.forEach(input => {
                    if (input === '&FILE_UPLOAD&'){
                        inputs.push(this.createDownloadFileBtn(dataType.files[0])) // #TODO: Make this so it takes the appropriate file (dropdown or smth in the future)
                    } else {
                        inputs.push(input + " ")
                    }
                });
            }
            return (
                    <React.Fragment>
                        {inputs.map((input) => (input))}
                    </React.Fragment>
                )
        }
    }];

    createDownloadFileBtn = (filePath) => {
        return (<Button key={filePath} hreftype="primary" file-path-index={filePath} icon="download"
                        size="small" style={{margin: '0 5px 0 5px'}}
                        onClick={(e) => {this.props.downloadFile(e.target.getAttribute('file-path-index'))}}>
                    Download File
                </Button>);
    };
 
    render() {
        const {conversation, dataTypes} = this.props;
        let typeFiles = {}
        //aggregate files by type
        for(let idx in conversation.Data.collectedData){
            let item = conversation.Data.collectedData[idx]
            if(item.input === "&FILE_UPLOAD&"){
                if(!typeFiles[item.dataType]){
                    typeFiles[item.dataType] = []
                }
                typeFiles[item.dataType].push(item.fileName)
            }
        }
        let realTypes = dataTypes.map(type => ({...type, files: typeFiles[type.name] ? typeFiles[type.name] : null}))
        return (
            conversation?.UserType !== "Unknown" ?
                <Table
                    columns={this.columns}
                    dataSource={realTypes.filter((type) => type.userTypes.includes(conversation.UserType))}
                    size='middle'
                    pagination={false}
                />
                : <Empty description={"Profile cannot be auto-generated for Unknown user type 😞"}/>
        );
    }
}
export default Profile;