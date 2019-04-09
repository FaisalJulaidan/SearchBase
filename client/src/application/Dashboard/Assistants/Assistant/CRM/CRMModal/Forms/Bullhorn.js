import React from 'react';
import {Typography, Icon, Input, InputNumber, Modal, Slider, Switch, Row, Col} from "antd";

import {getLink} from "helpers";

const BullhornFormItems = ({FormItem, layout, getFieldDecorator}) => {
    return (
        <div>
            <Row type="flex" justify="center">
                <img src={getLink('/static/images/undraw/comming_soon.svg')} alt="comming soon" height={300}
                     width={400}/>
            </Row>
            <Row type="flex" justify="center">
                <Typography.Text style={{color: 'grey', fontSize: 22}}>Coming Soon </Typography.Text>
            </Row>
        </div>
    )
};

export default BullhornFormItems