import React from "react";
import styles from "./SolutionsSettings.module.less";
import {Tabs, Form, Select, Button, Input, Switch} from "antd";
import QueueAnim from "rc-queue-anim";
import Animate from "rc-animate";
import {isEmpty} from "lodash";
import {profileActions} from "../../../../../../store/actions";
import ITDForm from "./InformationToDisplay/InformationToDisplay";
import BTForm from "./ButtonLink/ButtonLink";
import EAmForm from "./EmailAutomatch/EmailAutomatch";

const TabPane = Tabs.TabPane;

class SolutionsSettings extends React.Component{

    render (){

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
                        <Tabs defaultActiveKey={"1"}>

                            <TabPane tab={"Information to Display"} key={"1"}>
                                <ITDForm currentSolution={this.props.currentSolution} updateInformationToDisplay={this.props.updateInformationToDisplay}/>
                            </TabPane>

                            <TabPane tab={"Button Link"} key={"2"}>
                                <BTForm currentSolution={this.props.currentSolution} updateButtonLink={this.props.updateButtonLink}/>
                            </TabPane>

                            {/*<TabPane tab={"Results' Filters"} key={"3"}>*/}
                                {/*Coming soon...*/}
                            {/*</TabPane>*/}

                            <TabPane tab={"Email Auto-match"} key={"4"}>
                                <EAmForm sendSolutionAlerts={this.props.sendSolutionAlerts} submitAutomaticAlerts={(e) => {this.props.updateAutomaticAlerts(e)}}/>
                            </TabPane>

                        </Tabs>
                    }
                    </Animate>
                </div>
            </div>
        )
    }
}

export default Form.create()(SolutionsSettings)