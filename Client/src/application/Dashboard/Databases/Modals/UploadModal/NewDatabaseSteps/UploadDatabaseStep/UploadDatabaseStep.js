import { Button, Icon, message, Upload } from 'antd';
import React, { Component } from 'react';

import Worker from './excel.worker';

class UploadDatabaseStep extends Component {

    readExcel = () => { // returns a promise because reader is asynchronous function
        const { fileList, setStateHandler } = this.props;
        // This reads the file from the upload component
        // the file when uploaded as blob is considered as binary
        return new Promise((resolve, reject) => {
            if (fileList[0]) {
                setStateHandler({ isFileUploading: true });
                const reader = new FileReader();
                reader.readAsBinaryString(fileList[0]);
                reader.onload = () => {
                    const worker = new Worker();
                    worker.postMessage(reader.result);
                    worker.onmessage = (event) => {
                        setStateHandler({ isFileUploading: false });
                        if (event.data.headers)
                            return resolve(event.data);
                        else {
                            message.error('The uploaded size is too big');
                            return reject({
                                headers: undefined,
                                data: undefined
                            });
                        }
                    };
                };
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
        const { fileList, setStateHandler } = this.props;
        const props = {
            listType: 'picture',
            multiple: false,
            defaultFileList: [...fileList],
            accept: '.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel',
            onRemove: file => {
                setStateHandler((state) => {
                    const index = state.fileList.indexOf(file);
                    const newFileList = state.fileList.slice();
                    newFileList.splice(index, 1);
                    return {
                        fileList: newFileList
                    };
                });
            },
            beforeUpload: file => {
                file.thumbUrl = '/images/undraw/files.svg';
                setStateHandler(() => ({ fileList: [file] }));
                return false;
            },
            fileList
        };


        return (
            <div>
                <div style={{ textAlign: 'center' }}>
                    <img src={'/images/upload_data.svg'}
                         alt="Upload Data Iamge"
                         style={{ width: 300 }}/>
                    <p>Upload your Database to be used in the chat interaction</p>
                </div>
                <div style={{ textAlign: 'center' }}>
                    <Upload {...props}>
                        <Button>
                            <Icon type="upload"/> Upload
                        </Button>
                    </Upload>
                </div>
            </div>
        );
    }
}

export default UploadDatabaseStep;
