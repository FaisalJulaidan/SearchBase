import {Button, Icon, Upload} from "antd";
import React, {Component} from 'react';

class UploadDatabaseStep extends Component {
    tabJSON(csv) {
        let lines = eval('`' + csv + '`').split("\n");
        let result = [];
        let headers = lines[0].split("\t");
        for (let i = 1; i < lines.length; i++) {
            let obj = {};
            let currentline = lines[i].split("\t");
            for (let j = 0; j < headers.length; j++)
                obj[headers[j].trim()] = currentline[j].replace(/"/g, "");
            result.push(obj);
        }
        //return result; //JavaScript object
        return eval(JSON.stringify(result)); //JSON
    }

    render() {
        const {fileList, setStateHandler} = this.props;

        const handleUpload = () => {
            let reader = new FileReader();
            reader.readAsText(this.props.fileList[0]);
            reader.onload = () => {
                console.log(this.tabJSON(reader.result));
            }
        };

        const props = {
            listType: 'picture',
            multiple: false,
            defaultFileList: [...fileList],
            onRemove: (file) => {
                setStateHandler((state) => {
                    const index = state.fileList.indexOf(file);
                    const newFileList = state.fileList.slice();
                    newFileList.splice(index, 1);
                    return {
                        fileList: newFileList,
                    };
                });
            },
            beforeUpload: (file) => {
                file.thumbUrl = 'https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/files1_9ool.svg';
                setStateHandler(() => ({fileList: [file]}));
                return false;
            },
            fileList,
        };


        return (
            <div>
                <div style={{textAlign: 'center'}}>
                    <img src="http://localhost:5000/static/images/upload_data.svg" alt="Upload Data Iamge"
                         style={{width: 300}}/>
                    <p>Upload your Database to be used in the chat interaction</p>
                </div>
                <div style={{textAlign: 'center'}}>
                    <Upload {...props}>
                        <Button>
                            <Icon type="upload"/> Upload
                        </Button>
                    </Upload>
                    <Button onClick={handleUpload}>
                        Test
                    </Button>
                </div>
            </div>
        )
    }
}

export default UploadDatabaseStep;