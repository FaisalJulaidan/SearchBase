import {Button, Divider, Modal, Steps} from 'antd';

import React, {Component} from 'react';
import UploadDatabaseStep from './NewDatabaseSteps/UploadDatabaseStep'
import styles from "./NewDatabaseModal.module.less"
import ConfigureDatabaseStep from "./NewDatabaseSteps/UploadDatabaseStep/ConfigureDatabaseStep";

const Step = Steps.Step;

class NewDatabaseModal extends Component {

    constructor(props) {
        super(props);
        this.configureDatabaseStep = React.createRef();
    }

    state = {
        current: 0,
        fileList: [],
        uploading: false,
        databaseConfiguration: {
            databaseName: undefined,
            databaseType: undefined
        }
    };

    steps = [
        {
            title: 'Configre Database',
            content: () => <ConfigureDatabaseStep ref={this.configureDatabaseStep}
                                                  databaseConfiguration={this.state.databaseConfiguration}/>
        },
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


    next = () => {
        if (this.state.current + 1 === 1)
            this.configureDatabaseStep.current.validateFields(
                (err, values) => err ? null : this.setState({
                    databaseConfiguration: {
                        databaseName: values.databaseName,
                        databaseType: values.databaseType
                    },
                    current: this.state.current + 1
                })
            );
        else
            this.setState({current: this.state.current + 1})
    };

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

                <Divider/>

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