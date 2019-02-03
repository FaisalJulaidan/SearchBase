import {Button, Icon, Upload} from "antd";
import React, {Component} from 'react'


class UploadDatabaseStep extends Component {
    render() {
        const {uploading, fileList, setStateHandler} = this.props;

        const handleUpload = () => {
            const formData = new FormData();
            fileList.forEach((file) => {
                formData.append('files[]', file);
            });

            setStateHandler({
                uploading: true,
            });
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
                </div>
            </div>
        )
    }
}

export default UploadDatabaseStep;