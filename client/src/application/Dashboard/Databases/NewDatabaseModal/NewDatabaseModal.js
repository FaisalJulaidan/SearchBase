import {Button, Divider, Modal, Steps, Spin, message} from 'antd';

import React, {Component} from 'react';
import styles from "./NewDatabaseModal.module.less"

import UploadDatabaseStep from './NewDatabaseSteps/UploadDatabaseStep/UploadDatabaseStep'
import ConfigureDatabaseStep from "./NewDatabaseSteps/ConfigureDatabaseStep";
import ColumnSelectionStep from "./NewDatabaseSteps/ColumnSelectionStep";
import ConfirmStep from "./NewDatabaseSteps/ConfirmStep";
// import {dummyExcelData, jobsExcelSheet, validData, invalidData} from './testdata'

const Step = Steps.Step;

class NewDatabaseModal extends Component {

    constructor(props) {
        super(props);
        this.configureDatabaseStep = React.createRef();
        this.uploadDatabaseStep = React.createRef();
        this.columnSelectionStep = React.createRef();
    }

    state = {
        current: 0,
        fileList: [],

        databaseConfiguration: {
            databaseName: undefined,
            databaseType: undefined
        },

        isFileUploading: false,

        excelFile: {
            headers: undefined,
            data: undefined
        },

        validRecords: [],
        invalidRecords: []
    };

    steps = [
        {
            title: 'Configure Database',
            content: () => this.props.databaseOptions ?
                <ConfigureDatabaseStep ref={this.configureDatabaseStep}
                                       databaseOptions={this.props.databaseOptions}
                                       isDatabaseNameValid={this.props.isDatabaseNameValid}
                                       databaseConfiguration={this.state.databaseConfiguration}/>
                : <Spin/>
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
            content: () => this.props.databaseOptions ?
                <ColumnSelectionStep wrappedComponentRef={form => this.columnSelectionStep = form}
                                     databaseOptions={this.props.databaseOptions}
                                     databaseType={this.state.databaseConfiguration.databaseType}
                                     excelFile={this.state.excelFile}/>
                : <Spin/>
        },
        {
            title: 'Confirm ',
            content: () => this.props.databaseOptions ?
                <ConfirmStep validRecords={this.state.validRecords}
                             columns={this.props.databaseOptions[this.state.databaseConfiguration.databaseType]}
                             invalidRecords={this.state.invalidRecords}/>
                : <Spin/>
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
                this.columnSelectionStep.parseForm().then(
                    records => this.setState({
                        validRecords: records.validRecords,
                        invalidRecords: records.invalidRecords,
                        current: this.state.current + 1
                    }),
                    (error) => console.error(error)
                );
                break;

            default:
                this.setState({current: this.state.current + 1});
                break;
        }
    };

    prev = () => this.setState({current: this.state.current - 1});

    submitDatabase = () => {
        this.props.hideModal();
        const {validRecords, databaseConfiguration} = this.state;
        if (validRecords) {
            this.props.uploadDatabase({...databaseConfiguration, records: validRecords});
            // Reset state
            this.setState({
                current: 0,
                fileList: [],

                databaseConfiguration: {
                    databaseName: undefined,
                    databaseType: undefined
                },
                isFileUploading: false,
                excelFile: {
                    headers: undefined,
                    data: undefined
                },
                validRecords: [],
                invalidRecords: []
            })
        }
        else
            message.error('No valid records to be sent');
    };

    render() {
        const {current} = this.state;

        return (
            <Modal width={"80%"}
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
                            && <Button type="primary" onClick={this.submitDatabase}>Done</Button>
                        }
                    </div>
                </Spin>
            </Modal>
        );
    }
}

export default NewDatabaseModal;