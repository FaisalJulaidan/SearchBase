import React from 'react'

import {Modal, Form, Checkbox, Input, Button} from 'antd'

class CreateWebhookModal extends React.Component  {
    state = {
        webhook: {
            subscriptions: [],
            url: '',
            secret: null
        }
    }

    subscribeEvent = (status, eventName) => {
        const { subscriptions } = this.state.webhook
        this.setState({webhook: {...this.state.webhook, subscriptions: this.props.available.filter(event => event === eventName && status && !subscriptions.includes(eventName))}})
    }

    setWebhookAttribute = (key, attr) => this.setState({webhook: {...this.state.webhook, [key]: attr}})

    render() {
        const { url, subscriptions, secret } = this.state.webhook
        const usedList = subscriptions
        return(
            <Modal visible={this.props.visible} width={800} okText={"Create"}
                   onCancel={() => this.props.closeModal()}
                   onOk={() => this.props.create(this.state.webhook)}>
                <h3>Webhook information</h3>
                <Form>
                    <Form.Item label={"URL"}
                               help={"The URL the webhook points to, whenever the event occurs it will send a POST request to this URL with the appropriate data"}>
                        <Input type="text" value={url} onChange={(e) => this.setWebhookAttribute('url', e.target.value)}/>
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