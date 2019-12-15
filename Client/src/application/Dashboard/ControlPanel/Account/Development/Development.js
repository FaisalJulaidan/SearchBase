import React from 'react';

import { connect } from 'react-redux';
import { developmentActions } from 'store/actions';

import { Table, Button, Divider, Modal } from 'antd';

import EditWebhookModal from './EditWebhookModal';
import CreateWebhookModal from './CreateWebhookModal';

const { confirm } = Modal;

class Development extends React.Component {

    state = {
        activeID: null,
        showModal: false,
        createModal: false
    };

    modifyWebhook = (id) => {
        this.setState({ activeID: id, showModal: true });
    };

    deleteWebhook = (id) => {
        confirm({
            title: 'Are you sure you would like to delete this webhook?',
            onOk: () => {
                this.props.dispatch(developmentActions.deleteWebhookRequest(id));
            }
        });
    };

    componentDidUpdate(prevProps) {
        if (!this.props.isLoading && this.state.createModal && !this.props.errorMsg && this.props.webhooks.length > prevProps.webhooks.length) {
            this.setState({ createModal: false });
        }
    }

    closeModal = () => {
        this.setState({ showModal: false });
    };

    saveWebhook = (settings) => {
        this.props.dispatch(developmentActions.saveWebhookRequest(this.state.activeID, settings));
    };

    closeCreate = () => {
        this.setState({ createModal: false });
    };

    createWebhook = (settings) => {
        this.props.dispatch(developmentActions.createWebhookRequest(settings));
        // this.setState({createModal: false})
    };

    componentDidMount() {
        this.props.dispatch(developmentActions.fetchDevRequest());
    }

    render() {
        const webhookOptions = this.props.options.webhooks;
        const columns = [
            {
                title: 'URL',
                dataIndex: 'URL',
                key: 'URL'
            },
            {
                title: 'Subscriptions',
                dataIndex: 'Subscriptions',
                key: 'Subscriptions'
            },
            {
                title: 'Actions',
                key: 'actions',
                render: (text, record) => (
                    <span>
                        <a onClick={() => this.modifyWebhook(record.ID)}>Modify</a>
                        <Divider type="vertical"/>
                        <a onClick={() => this.deleteWebhook(record.ID)}>Delete</a>
                    </span>
                )
            }
        ];

        return (
            <>
                {this.props.webhooks && webhookOptions.availableWebhooks ?
                    <>
                        <div style={{ display: 'flex', marginBottom: 10 }}>
                            <h1 style={{ alignSelf: 'flex-start', margin: 0 }}>Webhooks</h1>
                            <Button style={{ alignSelf: 'flex-end', margin: '0 0 0 auto' }} icon={'plus'}
                                    onClick={() => this.setState({ createModal: true })}>Create</Button>
                        </div>
                        <Table
                            dataSource={this.props.webhooks}
                            columns={columns}
                        />
                        {this.state.activeID ?
                            <EditWebhookModal
                                webhook={this.props.webhooks.find(wh => wh.ID === this.state.activeID)}
                                visible={this.state.showModal}
                                closeModal={this.closeModal}
                                save={this.saveWebhook}
                                available={webhookOptions.availableWebhooks}/>
                            : null}
                        <CreateWebhookModal
                            visible={this.state.createModal}
                            closeModal={this.closeCreate}
                            create={this.createWebhook}
                            available={webhookOptions.availableWebhooks}/>
                    </>
                    : null}
            </>
        );
    }
}

// ,


function mapStateToProps(state) {
    return {
        webhooks: state.development.webhooks,
        options: state.options.options,
        isLoading: state.development.isLoading,
        errorMsg: state.development.errorMsg
    };
}

export default connect(mapStateToProps)(Development);
