import React, {Component} from 'react';
import "./Groups.less"
import styles from "../Flow.module.less";
import {Avatar, Button, Modal, List, Spin, Skeleton} from "antd";
import NewGroup from "./NewGroup/NewGroup";

const data = [
    {title: 'Greetings Group'},
    {title: 'Clients Group'},
    {title: 'Job Finders Group'},
    {title: 'Ending Group'}
];

class Groups extends Component {

    state = {visibleModal: false};

    handleOk = (e) => {
        console.log(e);
        this.setState({
            visibleModal: false,
        });
    };

    handleCancel = (e) => {
        console.log(e);
        this.setState({
            visibleModal: false,
        });
    };


    showModal = () => {
        this.setState({
            visibleModal: true,
        });
    };


    render() {
        return (
            <div className={styles.Panel}>
                <div className={styles.Header}>
                    <div>
                        <h3>Flow Groups</h3>
                    </div>
                    <div>
                        <Button className={styles.PanelButton} type="primary" icon="plus"
                                onClick={this.showModal}>
                            Add Group
                        </Button>

                        <Modal
                            width={800}
                            title="Create New Assistant"
                            visible={this.state.visibleModal}
                            onOk={this.handleOk}
                            onCancel={this.handleCancel}
                            footer={[
                                <Button key="cancle" onClick={this.handleCancel}>Cancle</Button>,
                                <Button key="submit" type="primary" onClick={this.handleOk}>
                                    Add
                                </Button>
                            ]}>
                            <NewGroup/>
                        </Modal>
                    </div>
                </div>


                <div className={styles.Body}>
                    {
                        this.props.isLoading ?
                            <Spin><Skeleton active={true}/></Spin>
                            :
                            <List
                                itemLayout="horizontal"
                                dataSource={this.props.groupsList}
                                renderItem={item => (
                                    <List.Item>
                                        <List.Item.Meta
                                            avatar={<Avatar icon="ordered-list"
                                                            style={{backgroundColor: '#9254de'}}/>}
                                            title={<a href="/">{item.name}</a>}
                                            description={item.description}
                                        />
                                    </List.Item>
                                )}
                            />
                    }
                </div>

            </div>
        );
    }
}

export default Groups;
