import React from 'react';
import {Button, Form, Modal, Row, Col, Tag, Tooltip} from "antd";

import {getLink} from "helpers";
import AdaptFormItems from "./Forms/Adapt"

import BullhornFormItems from "./Forms/Bullhorn"
import VincereFormItems from "./Forms/Vincere"
import AuroraCard from "components/AuroraCard/AuroraCard"

const FormItem = Form.Item;


class CRMModal extends React.Component {

    state = {
        Adapt: false,
        Bullhorn: false,
        Vincere: false
    };

    changeCRM = CRM => {
        const state = {...this.state};
        Object.keys(state).forEach((key) => {
            if (CRM === key)
                return state[key] = true;
            else
                return state[key] = false;
        });
        this.setState(state);
    };

    connectCRM = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            const state = {...this.state};
            this.props.handleConnect({
                type: Object.keys(state).find((CRM) => state[CRM] === true),
                auth: {...values},
            })
        }
    });

    testCRM = () => this.props.form.validateFields((err, values) => {
        if (!err) {
            const state = {...this.state};
            this.props.handleTest({
                type: Object.keys(state).find((CRM) => state[CRM] === true),
                auth: {...values},
            })
        }
    });


    disconnectCRM = () => {
        const state = {...this.state};
        this.props.handleDisconnect({
            type: Object.keys(state).find((CRM) => state[CRM] === true),
        })
    };

    render() {
        const layout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };

        const bullhornCard = <AuroraCard title={'Bullhorn'} selected={this.state.Bullhorn}
                                         onClick={() => this.changeCRM('Bullhorn')}
                                         image={getLink('/static/images/CRM/bullhorn.png')}
                                         selectImage={getLink('/static/images/CRM/select_bullhorn.png')}
                                         desc={<Tag color={this.state.Bullhorn ? "#9254de" : "grey"}>Coming
                                             Soon</Tag>}/>;

        const vencierCard = <AuroraCard title={'Vencier'} selected={this.state.Vincere}
                                        onClick={() => this.changeCRM('Vincere')}
                                        image={getLink('/static/images/CRM/vincere.png')}
                                        selectImage={getLink('/static/images/CRM/select_vincere.png')}
                                        desc={<Tag color={this.state.Vincere ? "#9254de" : "grey"}>Coming Soon</Tag>}/>

        const {getFieldDecorator} = this.props.form;

        return (
            <Modal title="CRM Integration"
                   visible={this.props.visible}
                   width={800}
                   destroyOnClose={true}
                   onCancel={this.props.handleCancel}
                   footer={[
                       <Button key="cancel" onClick={this.props.handleCancel}>Cancel</Button>,
                       this.props.assistant.CRMConnected ? null :
                           <Button key="test" type={this.props.isTestFaild ? 'danger' : 'default'}
                                   icon={this.props.isTestFails ? 'exclamation-circle' : ''}
                                   disabled={!this.state.Adapt}
                                   onClick={this.testCRM}>
                               Test
                           </Button>,
                       this.props.assistant.CRMConnected ?
                           <Button key="disconnect" type="danger"
                                   disabled={!this.state.Adapt}
                                   onClick={this.disconnectCRM}>
                               Disconnect
                           </Button> :
                           <Button key="submit" type="primary"
                                   disabled={!this.state.Adapt}
                                   onClick={this.connectCRM}>
                               Connect
                           </Button>,
                   ]}>

                <Row type="flex" justify="center" gutter={16}>
                    <Col span={6}>
                        <AuroraCard title={'Adapt'} selected={this.state.Adapt}
                                    onClick={() => this.changeCRM('Adapt')}
                                    image={getLink('/static/images/CRM/adapt.png')}
                                    selectImage={getLink('/static/images/CRM/select_adapt.png')}
                                    desc={<Tag color={this.state.Adapt ? "#9254de" : "#87d068"}>
                                        {this.props.assistant.CRMConnected ? 'Connected' : 'Connect Now'}</Tag>}/>
                    </Col>


                    <Col span={6}>
                        {
                            this.props.assistant.CRMConnected ?
                                <Tooltip title={`Disconnect from ${this.props.assistant.CRM} first`}>
                                    <div>
                                        {bullhornCard}
                                    </div>
                                </Tooltip>
                                : bullhornCard
                        }
                    </Col>

                    <Col span={6}>
                        {
                            this.props.assistant.CRMConnected ?
                                <Tooltip title={`Disconnect from ${this.props.assistant.CRM} first`}>
                                    <div>
                                        {vencierCard}
                                    </div>
                                </Tooltip>
                                : vencierCard
                        }
                    </Col>
                </Row>

                <br/>
                <br/>

                {
                    this.props.assistant.CRMConnected ? null :
                        <Form layout='horizontal'>
                            {
                                this.state.Adapt &&
                                <AdaptFormItems getFieldDecorator={getFieldDecorator}
                                                layout={layout}
                                                FormItem={FormItem}/>
                            }

                            {
                                this.state.Bullhorn &&
                                <BullhornFormItems getFieldDecorator={getFieldDecorator}
                                                   layout={layout}
                                                   FormItem={FormItem}/>
                            }

                            {
                                this.state.Vincere &&
                                <VincereFormItems getFieldDecorator={getFieldDecorator}
                                                  layout={layout}
                                                  FormItem={FormItem}/>
                            }
                        </Form>
                }

            </Modal>
        );
    }
}

export default Form.create()(CRMModal)
