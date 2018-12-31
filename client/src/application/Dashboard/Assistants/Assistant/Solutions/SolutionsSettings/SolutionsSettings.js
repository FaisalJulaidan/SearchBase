import React from "react";
import styles from "./SolutionsSettings.module.less";
import {Tabs, Form, Select, Button} from "antd";
import QueueAnim from "rc-queue-anim";

const TabPane = Tabs.TabPane;
const Option = Select.Option;
const FormItem = Form.Item;

class SolutionsSettings extends React.Component{

    state = {
        chosenDisplays: []
    };

    addNewDisplaySelect = () => {
        let chosenDisplays = [...this.state.chosenDisplays];
        chosenDisplays.push(undefined);
        this.setState({chosenDisplays: chosenDisplays});
    };

    render (){
        console.log(this.props);
        return(
            <div className={styles.Panel}>
                <div className={styles.Panel_Header}>
                    <div>
                        <h3 style={{height:"32px"}}>Solution Settings</h3>
                    </div>
                </div>


                <div className={styles.Panel_Body}>
                    <Tabs>

                        <TabPane tab={"Information to Display"} key={"1"}>
                            <Form style={{textAlign:"center"}}>
                                <p>From here you can choose which part of your information you want to be displayed inside the solution box.
                                    If you are unsure what data is inside those titles simply have a look at the Raw Data section.</p>
                                <Button className={styles.Button} type="primary" onClick={this.addNewDisplaySelect}>Add More Information</Button>
                                <QueueAnim>
                                {
                                    this.state.chosenDisplays.map((record, index) => {
                                        return (
                                            <Select className={styles.Select} key={index}>
                                                {/*{*/}
                                                    {/*this.state.chosenDisplays.map((record, index) => {*/}
                                                        {/*return <Option key={index} value={record}>{record}</Option>*/}
                                                    {/*})*/}
                                                {/*}*/}
                                            </Select>
                                        )
                                    })
                                }
                                </QueueAnim>
                            </Form>
                        </TabPane>

                        <TabPane tab={"Button Link"} key={"2"}/>

                        <TabPane tab={"Results' Filters"} key={"3"}/>

                        <TabPane tab={"Email Auto-match"} key={"4"}/>

                    </Tabs>
                </div>
            </div>
        )
    }
}

export default SolutionsSettings