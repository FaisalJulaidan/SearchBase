import React from 'react';
import {Button, Form, Modal, Row, Col, Tag} from "antd";

import AuroraCard from "components/AuroraCard/AuroraCard.js"
import {getLink} from "helpers";

import AdaptFormItems from "./Forms/Adapt"
import BullhornFormItems from "./Forms/Bullhorn"
import VincereFormItems from "./Forms/Vincere"

const FormItem = Form.Item;


class CRMModal extends React.Component {

    state = {
        adapt: false,
        bullhorn: false,
        vincere: false
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
                CRMType: Object.keys(state).find((CRM) => state[CRM] === true),
                details: {...values},
            })
        }
    });

    render() {
        const layout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };

        const {getFieldDecorator} = this.props.form;

        return (
            <Modal title="CRM Integration"
                   visible={this.props.visible}
                   width={800}
                   destroyOnClose={true}
                   onCancel={this.props.handleCancel}
                   footer={[
                       <Button key="cancel" onClick={this.props.handleCancel}>Cancel</Button>,
                       <Button key="submit" type="primary"
                               disabled={!this.state.adapt}
                               onClick={this.connectCRM}>
                           Connect
                       </Button>,
                   ]}>

                <Row type="flex" justify="center" gutter={16}>
                    <Col span={6}>
                        <AuroraCard title={'Adapt'} selected={this.state.adapt}
                                    onClick={() => this.changeCRM('adapt')}
                                    image={getLink('/static/images/CRM/adapt.png')}
                                    selectImage={getLink('/static/images/CRM/select_adapt.png')}
                                    desc={<Tag color={this.state.adapt ? "purple" : "#87d068"}>Connect Now</Tag>}/>
                    </Col>

                    <Col span={6}>
                        <AuroraCard title={'Bullhorn'} selected={this.state.bullhorn}
                                    onClick={() => this.changeCRM('bullhorn')}
                                    image={getLink('/static/images/CRM/bullhorn.png')}
                                    selectImage={getLink('/static/images/CRM/select_bullhorn.png')}
                                    desc={<Tag color={this.state.bullhorn ? "purple" : "grey"}>Coming Soon</Tag>}/>
                    </Col>

                    <Col span={6}>
                        <AuroraCard title={'Vencier'} selected={this.state.vincere}
                                    onClick={() => this.changeCRM('vincere')}
                                    image={getLink('/static/images/CRM/vincere.png')}
                                    selectImage={getLink('/static/images/CRM/select_vincere.png')}
                                    desc={<Tag color={this.state.vincere ? "purple" : "grey"}>Coming Soon</Tag>}/>
                    </Col>
                </Row>

                <br/>
                <br/>

                <Form layout='horizontal'>
                    {
                        this.state.adapt &&
                        <AdaptFormItems getFieldDecorator={getFieldDecorator}
                                        layout={layout}
                                        FormItem={FormItem}/>
                    }

                    {
                        this.state.bullhorn &&
                        <BullhornFormItems getFieldDecorator={getFieldDecorator}
                                           layout={layout}
                                           FormItem={FormItem}/>
                    }

                    {
                        this.state.vincere &&
                        <VincereFormItems getFieldDecorator={getFieldDecorator}
                                          layout={layout}
                                          FormItem={FormItem}/>
                    }
                </Form>
            </Modal>
        );
    }
}

export default Form.create()(CRMModal)
