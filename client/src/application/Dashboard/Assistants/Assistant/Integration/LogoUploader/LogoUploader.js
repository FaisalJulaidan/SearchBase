import React, {Component} from 'react';
import {croppedImg} from 'helpers/cropImage'

import {Button, Card, Icon, Modal, Upload} from 'antd';
import Cropper from 'react-easy-crop'
import styles from './LogoUploader.module.less'
import connect from "react-redux/es/connect/connect";
import {assistantActions} from "store/actions";

const Dragger = Upload.Dragger;

class LogoUploader extends Component {

    state = {
        assistant: {},
        mainFile: {},
        imageSrc: null,
        crop: {x: 0, y: 0},
        zoom: 1,
        aspect: 1,
        visible: false,

        croppedAreaPixels: null,
        croppedImage: null,

        timeStamp: new Date().getTime()
    };

    componentDidMount() {
    }

    componentWillReceiveProps(nextProps) {
        this.setState({assistant: nextProps.assistant, timeStamp: nextProps.msg});
    }


    onCropChange = crop => this.setState({crop});

    onCropComplete = (croppedArea, croppedAreaPixels) => this.setState({croppedAreaPixels});

    onZoomChange = zoom => this.setState({zoom});

    handleCancel = () => this.setState({visible: false});

    handleOk = async () => {
        const croppedImage = await croppedImg(this.state.imageSrc, this.state.croppedAreaPixels, this.state.mainFile.name);
        const formData = new FormData();
        formData.append('file', croppedImage);
        this.props.dispatch(assistantActions.uploadLogo(this.state.assistant?.ID, formData));
        this.setState({visible: false});
    };

    onFileChange = async e => {
        if (e) {
            const imageDataUrl = await readFile(e);
            this.setState({
                mainFile: e,
                imageSrc: imageDataUrl,
                crop: {x: 0, y: 0},
                zoom: 1,
                visible: true
            })
        }
    };

    deleteLogo = () => this.props.dispatch(assistantActions.deleteLogo(this.state.assistant?.ID));

    render() {
        // Warning: Auth leakage
        const props = {
            name: 'file',
            beforeUpload: file => {
                this.onFileChange(file);
                this.setState({visible: true});

                return false;
            },
            multiple: false,
            accept: 'image/png',
            showUploadList: false
        };
        const {assistant} = this.props;

        return (
            <div>

                <div style={{width: 300}}>
                    <h4>Logo uploader</h4>
                    <Dragger {...props}>
                        <p className="ant-upload-drag-icon">
                            <Icon type="inbox"/>
                        </p>
                        <p className="ant-upload-text">Click or drag file to this area to upload</p>
                        <p className="ant-upload-hint">
                            Support for a single or bulk upload. Strictly prohibit from uploading company data or other
                            band files
                        </p>
                    </Dragger>

                    {
                        assistant?.LogoName ?
                            <div>
                                <h4>The current logo</h4>
                                <Card hoverable
                                      style={{width: 300, textAlign: 'center'}}
                                      cover={<img alt="example"
                                                  src={`https://tsb.ams3.digitaloceanspaces.com/testing/companies_logo/${assistant?.LogoName}?timestamp=${this.state.timeStamp}`}/>}
                                >
                                    <Button type={'danger'} onClick={() => this.deleteLogo()}>Delete</Button>
                                </Card>
                            </div>
                            :
                            null
                    }
                </div>

                <Modal title="Basic Modal"
                       visible={this.state.visible}
                       onOk={this.handleOk}
                       onCancel={this.handleCancel}>
                    <div className={styles.CropContainer}>
                        <Cropper image={this.state.imageSrc}
                                 crop={this.state.crop}
                                 zoom={this.state.zoom}
                                 aspect={this.state.aspect}
                                 cropShape="round"
                                 showGrid={false}
                                 onCropChange={this.onCropChange}
                                 onCropComplete={this.onCropComplete}
                                 onZoomChange={this.onZoomChange}
                        />
                    </div>
                </Modal>

            </div>
        );
    }
}

function readFile(file) {
    return new Promise(resolve => {
        const reader = new FileReader();
        reader.addEventListener('load', () => resolve(reader.result), false)
        reader.readAsDataURL(file)
    })
}


const mapStateToProps = (state) => ({
    msg: state.assistant.successMsg,
});
export default connect(mapStateToProps)(LogoUploader);
