import React from "react";
import styles from "./SolutionsSettings.module.less";
import {Tabs, Form, Select, Button, Input, Icon} from "antd";
import QueueAnim from "rc-queue-anim";
import Animate from "rc-animate";
import {isEmpty} from "lodash";
import {profileActions} from "../../../../../../store/actions";

const TabPane = Tabs.TabPane;
const Option = Select.Option;
const FormItem = Form.Item;

class SolutionsSettings extends React.Component{

    state = {
        chosenDisplays: [],
        formSubmitted: false,
        tabIndex: 1
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.setState({formSubmitted: true});
                switch (this.state.tabIndex) {
                    case 1:
                        this.props.updateInformationToDisplay(values);
                        break;
                }
            }
        });
    };

    addNewDisplaySelect = () => {
        let chosenDisplays = [...this.state.chosenDisplays];
        chosenDisplays.push(undefined);
        this.setState({chosenDisplays: chosenDisplays});
    };

    changeTab = (key) => {
        this.setState({tabIndex: parseInt(key)});
    };

    renderInformationToDisplay(newProps){
        if(newProps.currentSolution.Solution === undefined){ return null; }
        if(newProps.currentSolution.Solution.DisplayTitles === null){ return null; }

        const chosenDisplays = [...newProps.currentSolution.Solution.DisplayTitles.titleValues];
        this.setState({chosenDisplays : chosenDisplays});
    }

    componentWillReceiveProps(newProps){
        if(!isEmpty(this.props.currentSolution)){
            if(this.props.currentSolution.Solution.ID === newProps.currentSolution.Solution.ID){ return null; }
            this.resetState();
        }
        this.renderInformationToDisplay(newProps);
    }

    resetState() {
        this.setState({
            chosenDisplays: [],
            formSubmitted: false,
            tabIndex: 1
        });
    }

    render (){
        const {getFieldDecorator} = this.props.form;
        console.log(this.props);
        return(
            <div className={styles.Panel}>
                <div className={styles.Panel_Header}>
                    <div>
                        <h3 style={{height:"32px"}}>Solution Settings</h3>
                    </div>
                </div>


                <div className={styles.Panel_Body}>
                    <Animate transitionName="fade" transitionAppear>
                    {isEmpty(this.props.currentSolution) ? null :
                        <Tabs defaultActiveKey={"1"} onChange={this.changeTab}>

                            <TabPane tab={"Information to Display"} key={"1"}>
                                <Form style={{textAlign:"center"}} onSubmit={this.handleSubmit}>
                                    <p>From here you can choose which part of your information you want to be displayed inside the solution box.
                                        If you are unsure what data is inside those titles simply have a look at the Raw Data section.</p>
                                    <Button className={styles.Button} type="primary" onClick={this.addNewDisplaySelect}>Add More Information</Button>
                                    <QueueAnim>
                                    {
                                        this.state.chosenDisplays.map((record, index) => {
                                            return (
                                                <FormItem style={{marginBottom: "5px"}} key={index}>
                                                    {getFieldDecorator("displaySelect" + String(index), {
                                                        initialValue: record,
                                                        rules: [{
                                                            required: true,
                                                            message: 'Please select a header',
                                                        }],
                                                    })(
                                                            <Select className={styles.Select}>
                                                                {
                                                                    this.props.currentSolution.DisplayTitles.map((record, index) => {
                                                                        return <Option key={index} value={record}>{record}</Option>
                                                                    })
                                                                }
                                                            </Select>
                                                    )}
                                                </FormItem>
                                            )
                                        })
                                    }
                                    </QueueAnim>
                                    <Button htmlType={"submit"} className={"ant-btn-primary"} style={{marginTop:"10px"}}>Update</Button>
                                </Form>
                            </TabPane>

                            <TabPane tab={"Button Link"} key={"2"}>
                                <Form style={{textAlign:"center"}}>
                                    <p>In order to be able to direct users to your solutions at your home website we will need some input from you.
                                        We would need the page part that holds all the solutions and then the solution reference. For example that
                                        can be http://mycoolwebsite.com/jobs/JobID* . To create the bridge between us we would need that information
                                        in the bellow text inputs. <br />
                                        <strong>To do that just contact us and we will find them for you.</strong><br />
                                        Alternatively you can try finding them on your own. To do that please provide us with the link (ex. \"http://mycoolwebsite.com/jobs/\")
                                        and then the reference to the JobID which you can find in your upload file(add @ in front of it) or Raw Data bellow.<br />
                                        For example: \"@JobDbID\" : C2143. <br />You can also take your solution ID and use Ctrl + F on this page to find the
                                        corresponding title in the Raw Data.</p>
                                </Form>
                            </TabPane>

                            <TabPane tab={"Results' Filters"} key={"3"}/>

                            <TabPane tab={"Email Auto-match"} key={"4"}/>

                        </Tabs>
                    }
                    </Animate>
                </div>
            </div>
        )
    }
}

export default Form.create()(SolutionsSettings)