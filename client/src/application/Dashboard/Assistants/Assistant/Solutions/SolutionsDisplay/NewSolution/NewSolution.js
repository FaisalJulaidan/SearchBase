import React from 'react';
import "./NewSolution.less"
import {Button, Modal, Form, Input, Select, Tabs, Icon, Upload} from "antd";

const FormItem = Form.Item;
const TabPane = Tabs.TabPane;
const OptGroup = Select.OptGroup;
const Option = Select.Option;

class NewSolution extends React.Component {

    state = {
        connectionType: "none",
        uploadFile: undefined
    };

    handleSave = () => this.props.form.validateFields((err, values) => {
        if (!err && this.state.uploadFile){
            values["uploadFile"] = this.state.uploadFile;
            const formData = new FormData();
            for (let key in values) {
                // skip loop if the property is from prototype
                if (!values.hasOwnProperty(key)) continue;

                formData.append(key, values[key]);
            }
            this.props.handleSave(formData);
            this.resetState();
        }
    });

    changeTypeHandler = (e) => {
        if (e === "RDB XML File Export") {
            this.setState({connectionType: "fileUpload"});
        }
        else if (e === "Bullhorn" || e === "RDB") {
            this.setState({connectionType: "CRMConnection"});
        } else {
            this.setState({connectionType: "none"});
        }
    };

    onFileChange = (e) => {
      const file = e.target.files[0];
      this.setState({uploadFile: file})
    };

    resetState = () => {
        this.setState({uploadFile: undefined, connectionType: "none"});
    };

    closeModal = () => {
        this.resetState();
        this.props.handleCancel();
    };

    render() {
        const formItemLayout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const {getFieldDecorator} = this.props.form;
        console.log(this.state);
        return (
            <Modal
                width={800}
                title="Create New Solution"
                destroyOnClose={true}
                visible={this.props.visible}
                onOk={this.props.handleSave}
                onCancel={this.props.handleCancel}
                footer={[
                    <Button key="Cancel" onClick={this.closeModal}>Cancel</Button>,
                    <Button key="submit" type="primary" onClick={this.handleSave}>
                        Add
                    </Button>
                ]}>
                <Form layout='horizontal'>
                    <FormItem
                        label="Solution Name"
                        extra="Enter a name for your solution to easily identify it in the solution list"
                        {...formItemLayout}>
                        {getFieldDecorator('name', {
                            rules: [{
                                required: true,
                                message: 'Please enter your solution name',
                            }],
                        })(
                            <Input placeholder="Ex: Jobs file, Bullhorn connection"/>
                        )}
                    </FormItem>

                    <FormItem
                        label="Solution Type"
                        extra="The type of File or CRM you want to connect"
                        {...formItemLayout}>
                        {getFieldDecorator('type', {
                            rules: [{
                                required: true,
                                message: 'Please select what type of connection you are making',
                            }],
                        })(
                            <Select onChange={this.changeTypeHandler}>
                                <OptGroup label={"File Upload"}>
                                    {
                                        this.props.databaseFileTypes.map(fileType => (
                                                <Option key={fileType} value={fileType}>{fileType}</Option>
                                            )
                                        )
                                    }
                                </OptGroup>
                                {/*<OptGroup label={"CRM Connection"}>*/}
                                    {/*{*/}
                                        {/*this.props.databaseCRMTypes.map(CRMType => (*/}
                                                {/*<Option key={CRMType} value={CRMType}>{CRMType}</Option>*/}
                                            {/*)*/}
                                        {/*)*/}
                                    {/*}*/}
                                {/*</OptGroup>*/}
                            </Select>
                        )}
                    </FormItem>

                    <Tabs activeKey={this.state.connectionType} tabBarStyle={{display:"none"}}>
                        <TabPane tab={"none"} key={"none"}>
                            <div style={{height: "86px", width:"752px"}}/>
                        </TabPane>
                        <TabPane tab={"fileUpload"} key={"fileUpload"}>
                            {/*<Button htmlFor={"fileUpload"}><Icon type={"upload"}/>Click to Upload</Button>*/}
                            <FormItem
                                label="Upload File"
                                extra="Select the file you wish to upload"
                                {...formItemLayout}>

                                <Input type={"file"} id={"fileUpload"} hidden={true} onChange={this.onFileChange}/>
                                <Button onClick={() => {document.getElementById("fileUpload").click()}}>
                                    <Icon type={"upload"}/>Select File
                                </Button> <label>{this.state.uploadFile ? this.state.uploadFile.name : "No File Chosen"}</label>

                            </FormItem>
                        </TabPane>
                        <TabPane tab={"CRMConnection"} key={"CRMConnection"}>
                            <FormItem
                                label="CRM Connection Link"
                                extra="Please paste your connection link"
                                {...formItemLayout}>
                                {getFieldDecorator('CRMLink', {
                                    rules: [{
                                        required: this.state.connectionType === "CRMConnection",
                                        message: 'Please paste the connection link for your CRM provided to you by us or your CRM manager',
                                    }],
                                })(
                                    <Input placeholder=""/>
                                )}
                            </FormItem>
                        </TabPane>
                    </Tabs>
                </Form>
            </Modal>
        );
    }
}

export default Form.create()(NewSolution)