import React from 'react';
import {Button, Icon, Input, InputNumber, Modal, Slider, Switch, Row, Col} from "antd";

import {getLink} from "helpers";

const BullhornFormItems = ({FormItem, layout, getFieldDecorator}) => {
    return (
        <div>
            <Button type="primary" icon={'login'}>Connect With Bullhorn</Button>
        </div>
    )
};

export default BullhornFormItems
