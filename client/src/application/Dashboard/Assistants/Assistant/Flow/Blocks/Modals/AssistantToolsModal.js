import React, {Component} from 'react';

import {Icon, Modal, Tabs} from 'antd';

import TextWebLink from "../Tools/TextWebLink";

const TabPane = Tabs.TabPane;

class AssistantToolsModal extends Component {

    state = {
        layout: {
            labelCol: {span: 6},
            wrapperCol: {span: 14}
        },
    };

    componentWillReceiveProps(nextProps) {
        console.log("nextProps: ", nextProps);
    }

    onChangeTab = (currentTab) => this.setState({currentTab});

    render() {
        return (
            <div>
                <Modal width={800}
                       title="Assistant tools"
                       visible={this.props.visible}
                       onCancel={this.props.closeModal}
                       destroyOnClose={true}
                       footer={null}>

                    <Tabs type="card" onChange={this.onChangeTab}>

                        <TabPane tab={<span><Icon type="font-colors"/>Text Web-Link</span>}
                                 key="text_web_link">
                            <TextWebLink formLayout={this.state.layout}/>
                        </TabPane>

                    </Tabs>
                </Modal>


            </div>
        );
    }
}


export default AssistantToolsModal;
