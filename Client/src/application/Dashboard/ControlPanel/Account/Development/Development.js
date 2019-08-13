import React from 'react';

import {Table} from 'antd'

class Development extends React.Component {

    state = {

    };

    modifyWebhook = (id) => {
        console.log(id)
    }

    deleteWebhook = (id) => {

        console.log(id)
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
           <Table
                dataSource={this.props.webhooks}
                columns={columns}
           />
        );
    }
}

export default Development;