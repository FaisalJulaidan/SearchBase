import React from 'react';

import {Table} from 'antd'
import EditWebhookModal from './EditWebhookModal'

class Development extends React.Component {

    state = {
        activeID: this.props.webhooks[0].ID,
        showModal: false
    };

    modifyWebhook = (id) => {
        this.setState({activeID: id, showModal: true})
    }

    deleteWebhook = (id) => {

    }

    saveWebhook = (settings) => {

    }

    componentDidMount = () => {
        console.log(this.props)
    }

    render() {
        const columns = [
            {
                title: "URL",
                dataIndex: "URL",
                key: "URL"
            },
            {
                title: "Subscriptions",
                dataIndex: "Subscriptions",
                key: "Subscriptions"
            },
            {
                title: "Actions",
                key: "actions",
                render: (text, record) => (
                    <span>
                        <button onClick={() => this.modifyWebhook(record.ID)}>Modify</button>
                        <button onClick={() => this.deleteWebhook(record.ID)}>Delete</button>
                    </span>
                )
            }
        ]
        return (
            <>
                <h1>Webhooks</h1>
               <Table
                    dataSource={this.props.webhooks}
                    columns={columns}
               />
               <EditWebhookModal
                     webhook={this.props.webhooks.find(wh => wh.ID === this.state.activeID)}
                    visible={this.state.showModal}
                     available={this.props.availablWebhooks}
                    save={this.saveWebhook}/>
           </>
        );
    }
}

export default Development;