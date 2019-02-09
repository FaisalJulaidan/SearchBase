import {Button, Divider, Modal, Steps, Spin} from 'antd';

import React, {Component} from 'react';
import UploadDatabaseStep from './NewDatabaseSteps/UploadDatabaseStep/UploadDatabaseStep'
import styles from "./NewDatabaseModal.module.less"
import ConfigureDatabaseStep from "./NewDatabaseSteps/ConfigureDatabaseStep";
import ColumnSelectionStep from "./NewDatabaseSteps/ColumnSelectionStep";
import {dummyExcelData} from './testdata'
const Step = Steps.Step;

class NewDatabaseModal extends Component {

    constructor(props) {
        super(props);
        this.configureDatabaseStep = React.createRef();
        this.uploadDatabaseStep = React.createRef();
        this.columnSelectionStep = React.createRef();
    }

    state = {
        current: 2,
        fileList: [],
        databaseConfiguration: {
            databaseName: 'abc',
            databaseType: 'Jobs'
        },

        isFileUploading: false,

        excelFile: {
            headers: dummyExcelData.headers,
            // headers: undefined,
            // data: undefined
            data: dummyExcelData.data
        }
    };

    steps = [
        {
            title: 'Configre Database',
            content: () => <ConfigureDatabaseStep ref={this.configureDatabaseStep}
                                                  databaseOptions={this.props.databaseOptions}
                                                  databaseConfiguration={this.state.databaseConfiguration}/>
        },
        {
            title: 'Upload Data',
            content: () => <UploadDatabaseStep ref={this.uploadDatabaseStep}
                                               uploading={this.state.uploading}
                                               handleUpload={this.handleUpload}
                                               setStateHandler={state => this.setState(state)}
                                               fileList={this.state.fileList}/>
        },
        {
            title: 'Column Selection',
            content: () => <ColumnSelectionStep wrappedComponentRef={form => this.columnSelectionStep = form}
                                                databaseOptions={this.props.databaseOptions}
                                                databaseType={this.state.databaseConfiguration.databaseType}
                                                excelFile={this.state.excelFile}/>,
        },
        {
            title: 'Last',
            content: () => 'Last-content',
        }];


    next = () => {
        switch (this.state.current + 1) {
            case 1:
                this.configureDatabaseStep.current.validateFields(
                    (err, values) => err ? null : this.setState({
                        databaseConfiguration: {
                            databaseName: values.databaseName,
                            databaseType: values.databaseType
                        },
                        current: this.state.current + 1
                    })
                );
                break;

            case 2:
                this.uploadDatabaseStep.current.readExcel().then(
                    excelFile => {
                        console.log(JSON.stringify(excelFile));
                        this.setState({excelFile, current: this.state.current + 1})
                    },
                    rejectedExcelFile => this.setState({excelFile: rejectedExcelFile})
                );
                break;

            case 3:
                this.columnSelectionStep.parseForm();
                break;

            default:
                this.setState({current: this.state.current + 1});
                break;
        }
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
                <Spin spinning={this.state.isFileUploading} tip="Reading Excel File">

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
                </Spin>
            </Modal>

        );
    }
}

export default NewDatabaseModal;