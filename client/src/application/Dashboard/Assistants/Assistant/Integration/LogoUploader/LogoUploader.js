import React, {Component} from 'react';
import {authHeader} from 'helpers'

import {Button, Card, Icon, message, Upload} from 'antd';

const {Meta} = Card;

class LogoUploader extends Component {

    state = {
        assistant: {}
    };

    componentDidMount() {
    }

    componentWillReceiveProps(nextProps) {
        this.setState({assistant: nextProps.assistant});
    }

    render() {
        // Warning: Auth leakage
        const props = {
            name: 'file',
            action: `http://localhost:3000/api/assistant/${this.state.assistant?.ID}/logo`,
            headers: {
                ...authHeader()
            },
            onChange(info) {
                if (info.file.status !== 'uploading') {
                    console.log(info.file, info.fileList);
                }
                if (info.file.status === 'done') {
                    message.success(`${info.file.name} file uploaded successfully`);
                } else if (info.file.status === 'error') {
                    message.error(`${info.file.name} file upload failed.`);
                }
            },
        };
        return (
            <div>
                <h1>This is uploader</h1>
                {
                    this.state.assistant.LogoName &&
                    <Card
                        style={{width: 300, textAlign: 'center'}}
                        cover={
                            <img alt="example"
                                 src={`https://tsb.ams3.digitaloceanspaces.com/testing//chatbot_logos/${this.state.assistant.LogoName}`}
                            />
                        }
                    >
                        <Button type={'danger'}>Delete</Button>
                    </Card>
                }

                <Upload {...props}>
                    <Button>
                        <Icon type="upload"/> Click to Upload
                    </Button>
                </Upload>
            </div>
        );
    }
}


export default LogoUploader;
