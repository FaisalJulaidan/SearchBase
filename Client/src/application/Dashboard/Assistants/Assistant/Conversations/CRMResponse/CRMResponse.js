import React, {Component} from 'react';
import {Button, Table, Tag} from "antd";

import {Typography} from 'antd';

const {Text} = Typography;

class CRMResponse extends Component {

    state = {};

    render() {
        const {conversation} = this.props;
        return (
            conversation.CRMResponse ?
                <div>
                    <h3>
                        CRM Status:
                        <Tag color={conversation.CRMSynced ? "#87d068" : "red"}
                             style={{marginLeft: 5}}>
                            {conversation.CRMSynced ? 'Success' : 'Failed'}
                        </Tag>
                    </h3>

                    <br/>

                    <h3>CRM Response:
                        <Text code>
                            {conversation.CRMResponse}
                        </Text></h3>
                </div> : null
        );
    }
}

export default CRMResponse;
