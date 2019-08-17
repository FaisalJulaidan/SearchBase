import React from 'react'

import {Modal, Form, Checkbox, Input, Select} from 'antd'

const { Option } = Select

class CreateWebhookModal extends React.Component  {
    state = {
        webhook: {
            subscriptions: [],
            url: '',
            secret: null,
            protocol: "http://"
        }
    }

    subscribeEvent = (status, eventName) => {
        const { subscriptions } = this.state.webhook
        this.setState({webhook: {...this.state.webhook, subscriptions: this.props.available.filter(event => event === eventName && status && !subscriptions.includes(eventName))}})
    }

    setWebhookAttribute = (key, attr) => this.setState({webhook: {...this.state.webhook, [key]: attr}})

    create = () => {
        const { url, protocol, subscriptions, secret } = this.state.webhook
        console.log(protocol)
        this.props.create({
            url: protocol + url,
            subscriptions,
            secret
        })
    }

    render() {
        const { url, subscriptions, secret, protocol } = this.state.webhook
        const usedList = subscriptions

        const selectBefore = (
            <Select value={protocol} style={{ width: 90 }} onChange={e => this.setWebhookAttribute('protocol', e)}>
                <Option value="http://">http://</Option>
                <Option value="https://">https://</Option>
            </Select>
        );

        return(
            <Modal visible={this.props.visible} width={800} okText={"Create"}
                   onCancel={() => this.props.closeModal()}
                   onOk={() => this.create()}>
                <h3>Webhook information</h3>
                <Form>
                    <Form.Item label={"URL"}
                               help={"The URL the webhook points to, whenever the event occurs it will send a POST request to this URL with the appropriate data"}>
                        <Input addonBefore={selectBefore} type="text" value={url} onChange={(e) => this.setWebhookAttribute('url', e.target.value)}/>
                    </Form.Item>
                    <Form.Item label={"Events"}
                               help={"The events you'd like to subscribe to for this webhook"}>
                        {this.props.available.map((webhook, i) => (
                            <Checkbox key={i} checked={usedList.includes(webhook)} onChange={(e) => this.subscribeEvent(e.target.checked, webhook)}>{webhook}</Checkbox>
                        ))}
                    </Form.Item>
                    <Form.Item label={"Secret"}
                               help={"The secret is optional, and if provided when sent to the address specified, it will be sent SHA256 encoded"}>
                        <Input type="text" value={secret} onChange={e =>  this.setWebhookAttribute('secret', e.target.value === "" ? null : e.target.value)} />
                    </Form.Item>
                </Form>
            </Modal>
        )
    }
}

export default CreateWebhookModal