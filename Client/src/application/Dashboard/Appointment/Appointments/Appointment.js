import React from 'react'
import App from "../../../../App"
import { List, Col } from 'antd'

class Appointment extends React.Component {
    render() {
        return (
            <List.Item>
                <Col span={6}>
                    {this.props.with}
                </Col>
                <Col span={6}>
                    status {this.props.status}
                </Col>
                <Col span={3}>
                    status {this.props.status}
                </Col>
                <Col span={3}>
                    status {this.props.status}
                </Col>

            </List.Item>
        )
    }

}

export default Appointment
