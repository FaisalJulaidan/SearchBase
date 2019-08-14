import React from 'react';

import {connect} from 'react-redux'
import {developmentActions} from "store/actions/development.actions";

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

    closeModal = () => {
        this.setState({showModal: false})
    }

    saveWebhook = (settings) => {
        this.props.dispatch(developmentActions.saveWebhookRequest(this.state.activeID, settings))
    }

    componentDidMount = () => {
        console.log(this.props)
        this.props.dispatch(developmentActions.fetchDevRequest())
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
                    closeModal={this.closeModal}
                    save={this.saveWebhook}
                    available={this.props.availableWebhooks} />
           </>
        );
    }
}

// ,


function mapStateToProps(state) {
    return {
        webhooks: state.development.webhooks,
        availableWebhooks: state.development.availableWebhooks
    };
}

export default connect(mapStateToProps)(Development);
