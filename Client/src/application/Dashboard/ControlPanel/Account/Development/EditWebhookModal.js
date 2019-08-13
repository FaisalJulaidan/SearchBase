import React from 'react'

import {Modal, Form, Checkbox, Input} from 'antd'

class EditWebhookModal extends React.Component {
    render() {
        const { webhook } = this.props
        const usedList = webhook.Subscriptions.split(',')
        console.log(this.props)
        return(
            <Modal visible={this.props.visible}>
                <h3>Webhook information</h3>
                <Form>
                    <Form.Item label={"URL"}
                               help={"The URL the webhook points to, whenever the event occurs it will send a POST request to this URL with the appropriate data"}>
                        <Input type="text" defaultValue={webhook.URL} />
                    </Form.Item>
                    <Form.Item label={"Events"}
                               help={"The events you'd like to subscribe to for this specific webhook"}>
                        {this.props.available.map(webhook => (
                            <Checkbox defaultChecked={usedList.includes(webhook)}>{webhook}</Checkbox>
                        ))}
                    </Form.Item>
                </Form>
            </Modal>
        )
    }
}

export default EditWebhookModal