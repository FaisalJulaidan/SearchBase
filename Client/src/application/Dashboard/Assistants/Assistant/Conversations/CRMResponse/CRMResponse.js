import React, {Component} from 'react';
import {Empty, Tag, Typography} from "antd";

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

                    <h3>CRM Response:</h3>
                    <Text>
                            {conversation.CRMResponse}
                    </Text>
                </div> : <Empty description={'CRM was not connected'}/>
        );
    }
}

export default CRMResponse;
