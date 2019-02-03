import {Button, Modal, Steps} from 'antd';

import React, {Component} from 'react';
import UploadDatabaseStep from './NewDatabaseSteps/UploadDatabaseStep'
import styles from "./NewDatabaseModal.module.less"

const Step = Steps.Step;


class NewDatabaseModal extends Component {

    state = {
        current: 0,
        fileList: [],
        uploading: false,
    };

    steps = [
        {
            title: 'Upload Data',
            content: () => <UploadDatabaseStep uploading={this.state.uploading}
                                               handleUpload={this.handleUpload}
                                               setStateHandler={(state) => this.setState(state)}
                                               fileList={this.state.fileList}/>
        },
        {
            title: 'Second',
            content: () => 'Second-content',
        },
        {
            title: 'Last',
            content: () => 'Last-content',
        }];


    next = () => this.setState({current: this.state.current + 1});
    prev = () => this.setState({current: this.state.current - 1});

    render() {
        const {current} = this.state;

        return (
            <Modal
                width={800}
                title="Upload New Database"
                visible={this.props.visible}
                onCancel={this.props.hideModal}
                destroyOnClose={true}
                footer={null}>

                <Steps current={current}>
                    {this.steps.map(item => <Step key={item.title} title={item.title}/>)}
                </Steps>

                <div className={styles.steps_content}>{this.steps[current].content()}</div>

                <div className={styles.steps_action}>
                    {
                        current > 0
                        && (
                            <Button style={{marginLeft: 8}} onClick={() => this.prev()}>
                                Previous
                            </Button>
                        )
                    }
                    {
                        current < this.steps.length - 1
                        && <Button type="primary" onClick={() => this.next()}>Next</Button>
                    }
                    {
                        current === this.steps.length - 1
                        && <Button type="primary" onClick={this.props.hideModal}>Done</Button>
                    }
                </div>
            </Modal>
        );
    }
}

export default NewDatabaseModal;