import React, {Component} from 'react';

import "./BlocksDrawer.less"
import styles from "./BlocksDrawer.module.less";

import {Form, Icon, Tabs} from "antd";

import UserInput from "./Cards/UserInput";
import Question from "./Cards/Question";
import FileUpload from "./Cards/FileUpload";
import Solutions from "./Cards/Solutions";
import GoToBlock from "./Cards/GoToBlock";
import GoToGroup from "./Cards/GoToGroup";

const TabPane = Tabs.TabPane;


const formItemLayout = {
    labelCol: {span: 6},
    wrapperCol: {span: 14},
};

class Blocks extends Component {

    state = {};

    render() {
        return (
            <Tabs type="card" tabPosition={'right'}>

                <TabPane tab={<span><Icon type="form"/>User Input</span>}
                         key="1">
                    <UserInput layout={formItemLayout} onClose={this.props.onClose}/>
                </TabPane>

                <TabPane tab={<span><Icon type="question-circle"/>Question</span>}
                         key="2">
                    <Question layout={formItemLayout} onClose={this.props.onClose}/>
                </TabPane>

                <TabPane tab={<span><Icon type="file-add"/>File Upload</span>}
                         key="3">
                    <FileUpload layout={formItemLayout} onClose={this.props.onClose}/>
                </TabPane>

                <TabPane tab={<span><Icon type="tag"/>Solutions</span>}
                         key="4">
                    <Solutions layout={formItemLayout} onClose={this.props.onClose}/>
                </TabPane>

                <TabPane tab={<span><Icon type="branches"/>Go to block</span>}
                         key="5">
                    <GoToBlock layout={formItemLayout} onClose={this.props.onClose}/>
                </TabPane>

                <TabPane tab={<span><Icon type="fork"/>Go to group</span>}
                         key="6">
                    <GoToGroup layout={formItemLayout} onClose={this.props.onClose}/>
                </TabPane>

            </Tabs>
        );
    }
}

export default Form.create()(Blocks);
