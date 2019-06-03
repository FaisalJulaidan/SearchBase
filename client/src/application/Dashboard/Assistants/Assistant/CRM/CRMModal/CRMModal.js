import React from 'react';
import {Button, Form, Modal, Radio, Row} from "antd";
import {history} from "helpers";

const FormItem = Form.Item;

const RadioButton = Radio.Button;
const RadioGroup = Radio.Group;


class CRMModal extends React.Component {

    state = {
        selectedCRM: 0
    };

    componentDidMount() {
        this.setState({selectedCRM: this.props.assistant?.CRMID})

    }


    updateSelectedCRM = event => this.setState({selectedCRM: event.target.value});

    resetSelectedCRM = () => {
        this.setState({selectedCRM: null});
        this.props.handleReset()
    };

    render() {
        return (
            <Modal title="CRM Integration"
                   visible={this.props.visible}
                   width={800}
                   destroyOnClose={true}
                   onCancel={this.props.handleCancel}
                   footer={[
                       <Button key="connect" onClick={() => {
                           this.props.handleCancel();
                           history.push(`/dashboard/crmlist`);
                       }}>Connect New
                           CRM</Button>,
                       <Button key="submit" type="primary"
                               onClick={() => this.props.handleSave(this.state.selectedCRM)}>Save</Button>,
                       <Button key="reset" type="danger" onClick={this.resetSelectedCRM}>Reset All</Button>,
                   ]}
            >

                <h3>Select a CRM to link it with this assistant</h3>
                <p>If nothing shows, navigate to CRMs List to connect your account</p>
                <Row type="flex" justify="center">
                    <RadioGroup value={this.state.selectedCRM} onChange={this.updateSelectedCRM}>
                        {
                            this.props.CRMsList[0] &&
                            this.props.CRMsList.map(
                                (CRM, i) => <RadioButton key={i} value={CRM.ID}>{CRM.Type}</RadioButton>
                            )
                        }

                        {
                            !this.props.CRMsList[0] &&
                            <RadioButton value={''} disabled>Connect New CRM Below</RadioButton>
                        }
                    </RadioGroup>
                </Row>

            </Modal>
        );
    }
}

export default Form.create()(CRMModal)
