import React, {Component} from 'react';
import {Button, Modal} from 'antd';


import "./Assistants.less"
import styles from "./Assistants.module.less"
import Assistant from "../Assistant/Assistant"

import NewRequest from "./NewAssistant/NewRequest"

class Assistants extends Component {
    state = {};
    arr = Array(15).fill(0);

    state = {visible: false};

    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    handleOk = (e) => {
        console.log(e);
        this.setState({
            visible: false,
        });
    };

    handleCancel = (e) => {
        console.log(e);
        this.setState({
            visible: false,
        });
    };

    render() {
        return (

            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Header}>
                        <div>
                            <h3>Assistants List</h3>
                            <p>Here you can see all assistants created by you</p>
                        </div>
                        <div>
                            <Button className={styles.AddAssistant} type="primary" icon="plus" onClick={this.showModal}>
                                Add Assistant
                            </Button>
                        </div>

                    </div>


                    <div className={styles.Body}>
                        <div className={styles.AssistantsList}>
                            {this.arr.map((x, i) => <Assistant key={i} index={i}/>)}
                        </div>
                    </div>

                </div>

                <Modal
                    width={800}
                    title="Create New Assistant"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    footer={[
                        <Button key="cancle" onClick={this.handleCancel}>Cancle</Button>,
                        <Button key="submit" type="primary" onClick={this.handleOk}>
                            Submit
                        </Button>,
                    ]}
                >
                    <NewRequest/>
                </Modal>
            </div>
        );
    }
}

export default Assistants;
