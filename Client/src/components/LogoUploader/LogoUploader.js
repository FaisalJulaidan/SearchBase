import React, { Component } from 'react';
import { croppedImg } from 'helpers/cropImage';

import { Button, Card, Icon, Modal, Upload } from 'antd';
import Cropper from 'react-easy-crop';
import styles from './LogoUploader.module.less';

const Dragger = Upload.Dragger;

class LogoUploader extends Component {
    state = {
        mainFile: {},
        imageSrc: null,
        crop: { x: 0, y: 0 },
        zoom: 1,
        aspect: 1,
        visible: false,

        croppedAreaPixels: null,
        croppedImage: null,

        timeStamp: new Date().getTime()
    };

    componentWillReceiveProps(nextProps) {
        this.setState({ timeStamp: new Date().getTime() });
    }

    onCropChange = crop => this.setState({ crop });

    onCropComplete = (croppedArea, croppedAreaPixels) =>
        this.setState({ croppedAreaPixels });

    onZoomChange = zoom => this.setState({ zoom });

    handleCancel = () => this.setState({ visible: false });

    handleOk = async () => {
        const croppedImage = await croppedImg(
            this.state.imageSrc,
            this.state.croppedAreaPixels,
            this.state.mainFile.name
        );
        const formData = new FormData();
        formData.append('file', croppedImage);
        this.props.uploadLogo(formData);
        this.setState({ visible: false });
    };

    onFileChange = async e => {
        if (e) {
            const imageDataUrl = await readFile(e);
            this.setState({
                mainFile: e,
                imageSrc: imageDataUrl,
                crop: { x: 0, y: 0 },
                zoom: 1,
                visible: true
            });
        }
    };

    deleteLogo = () => this.props.deleteLogo();

    render() {
        // Warning: Auth leakage
        const props = {
            name: 'file',
            beforeUpload: file => {
                this.onFileChange(file);
                this.setState({ visible: true });

                return false;
            },
            multiple: false,
            accept: 'image/png',
            showUploadList: false
        };
        const { logoPath } = this.props;
        return (
            <div>
                <div style={{ width: 300 }}>
                    <Dragger {...props}>
                        <p className="ant-upload-drag-icon"> 
                            <Icon type="inbox" />
                        </p>
                        <p className="ant-upload-text">
                            Click or drag file to this area to upload
                        </p>
                        <p className="ant-upload-hint">
                            Support for a single or bulk upload. Strictly
                            prohibit from uploading company data or other band
                            files
                        </p>
                    </Dragger>

                    {logoPath ? (
                        <div>
                            <h3>The current logo</h3>
                            <Card
                                hoverable
                                style={{ width: 300, textAlign: 'center' }}
                                cover={
                                    <img
                                        alt="example"
                                        src={`${logoPath}?timestamp=${this.state.timeStamp}`}
                                    />
                                }
                            >
                                <Button
                                    type={'danger'}
                                    onClick={() => this.deleteLogo()}
                                >
                                    Delete
                                </Button>
                            </Card>
                        </div>
                    ) : null}
                </div>

                <Modal
                    title="Resize your image"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                >
                    <div className={styles.CropContainer}>
                        <Cropper
                            image={this.state.imageSrc}
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
        reader.addEventListener('load', () => resolve(reader.result), false);
        reader.readAsDataURL(file);
    });
}

export default LogoUploader;
