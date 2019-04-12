import React, {Component} from 'react';
import {Button, Table, Tag} from "antd";

import {Typography} from 'antd';

const {Text} = Typography;

class CRMResponse extends Component {

    state = {};

    render() {
        const {session} = this.props;
        return (
            session.CRMSynced && session.CRMResponse ?
                <div>
                    <h3>
                        CRM Status:
                        <Tag color={session.CRMSynced ? "#87d068" : "red"}
                             style={{marginLeft: 5}}>
                            {session.CRMSynced ? 'Sucess' : 'Failed'}
                        </Tag>
                    </h3>

                    <br/>

                    <h3>CRM Response:
                        <Text code>
                            {session.CRMResponse}
                        </Text></h3>
                </div> : null
        );
    }
}

export default CRMResponse;
