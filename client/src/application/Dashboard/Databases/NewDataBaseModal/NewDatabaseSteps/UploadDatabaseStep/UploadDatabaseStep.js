import {Button, Icon, Upload, message} from "antd";
import React, {Component} from 'react';
import XLSX from 'xlsx';

class UploadDatabaseStep extends Component {

    readExcel = () => { // returns a promise because reader is asynchronous function
        const {fileList} = this.props;
        // This reads the file from the upload component
        // the file when uploaded as blob is considered as binary
        return new Promise((resolve, reject) => {
            if (fileList[0]) {
                const reader = new FileReader();
                reader.readAsBinaryString(fileList[0]);
                reader.onload = () => {
                    const workbook = XLSX.read(reader.result, {type: 'binary'});
                    const first_worksheet = workbook.Sheets[workbook.SheetNames[0]];
                    /* DO SOMETHING WITH workbook HERE */
                    return resolve({
                        headers: XLSX.utils.sheet_to_json(first_worksheet, {header: 1})[0],
                        data: XLSX.utils.sheet_to_json(first_worksheet)
                    });
                }
            } else {
                message.error('Please upload Excel file or CSV file');
                return reject({
                    headers: undefined,
                    data: undefined
                });
            }
        });
    };

    render() {
        const {fileList, setStateHandler} = this.props;
        const props = {
            listType: 'picture',
            multiple: false,
            defaultFileList: [...fileList],
            accept:".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel",
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
                    {/*<Upload.Dragger {...props}>*/}
                    {/*<p className="ant-upload-drag-icon">*/}
                    {/*<Icon type="inbox"/>*/}
                    {/*</p>*/}
                    {/*<p className="ant-upload-text">Click or drag file to this area to upload</p>*/}
                    {/*<p className="ant-upload-hint">Support for a single or bulk upload. Strictly prohibit from*/}
                    {/*uploading company data or other band files</p>*/}

                    {/*</Upload.Dragger>*/}

                    {/*<Button onClick={handleUpload}>*/}
                    {/*Test*/}
                    {/*</Button>*/}
                </div>
            </div>
        )
    }
}

export default UploadDatabaseStep;