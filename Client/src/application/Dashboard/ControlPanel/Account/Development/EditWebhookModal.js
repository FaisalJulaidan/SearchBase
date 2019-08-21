import React from 'react'

import {Modal, Form, Checkbox, Input, Select} from 'antd'
const { Option } = Select

class EditWebhookModal extends React.Component  {
    constructor(props){
        super(props)
        let protocol = this.props.webhook.URL.match(new RegExp(`^https?://`))
        this.state = {
            webhook: {
                subscriptions: this.props.webhook.Subscriptions.split(','),
                url: this.props.webhook.URL.replace(protocol, ''),
                secret: this.props.webhook.hasSecret ? "" : null,
                protocol
            }
        }
    }



    save = () => {
        const { url, protocol, subscriptions, secret } = this.state.webhook
        console.log(protocol)
        this.props.save({
            url: protocol + url,
            subscriptions,
            secret
        })
    }

    subscribeEvent = (status, eventName) => {
        const { subscriptions } = this.state.webhook
        this.setState({webhook: {...this.state.webhook, subscriptions: this.props.available.filter(event => event === eventName && status && !subscriptions.includes(eventName))}})
    }

    setWebhookAttribute = (key, attr) => this.setState({webhook: {...this.state.webhook, [key]: attr}})

    render() {
        console.log(this.state.webhook)

        const { url, subscriptions, secret, protocol } = this.state.webhook
        const { isLoading } = this.props.webhook
        const usedList = subscriptions

        const selectBefore = (
            <Select value={protocol} style={{ width: 90 }} onChange={e => this.setWebhookAttribute('protocol', e)}>
                <Option value="http://">http://</Option>
                <Option value="https://">https://</Option>
            </Select>
        );

        return(
            <Modal visible={this.props.visible} width={800} okText={"Save"}
                   onCancel={() => this.props.closeModal()}
                   okButtonProps={{loading: isLoading}}
                   onOk={() => this.save()}>
                <h3>Webhook information</h3>
                <Form>
                    <Form.Item label={"URL"}
                               help={"The URL the webhook points to, whenever the event occurs it will send a POST request to this URL with the appropriate data"}>
                        <Input type="text" addonBefore={selectBefore} value={url} onChange={(e) => this.setWebhookAttribute('url', e.target.value)}/>
                    </Form.Item>
                    <Form.Item label={"Events"}
                               help={"The events you'd like to subscribe to for this webhook"}>
                    {this.props.available.map((webhook, i) => (
                        <Checkbox key={i} checked={usedList.includes(webhook)} onChange={(e) => this.subscribeEvent(e.target.checked, webhook)}>{webhook}</Checkbox>
                    ))}
                    </Form.Item>
                    <Form.Item label={"Secret"}
                               help={"If you would like to keep the secret as is, please leave this field empty, otherwise put in a new secret"}>
                        <Input type="text" value={secret} onChange={e =>  this.setWebhookAttribute('secret', e.target.value)} />
                    </Form.Item>
                </Form>
            </Modal>
        )
    }
}

export default EditWebhookModal