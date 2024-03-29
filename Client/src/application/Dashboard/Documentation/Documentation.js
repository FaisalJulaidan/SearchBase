import React from "react";
import Header from "../../../components/Header/Header";
import {Menu, Icon, Tabs, Button} from 'antd';
import styles from "./Documentation.module.less";

const SubMenu = Menu.SubMenu;
const TabPane = Tabs.TabPane;

class Documentation extends React.Component{

    state = {
        currentKey: "1"
    };

    handleMenuChange = (item) => {
        this.setState({currentKey: item.key});
    };

    render () {


        return (
            <div style={{height: '100%'}}>
                <div style={{height: 'calc(100% - 66px)', width: '100%', display: 'flex'}}>
                    <div style={{margin: 5, width: '27%'}}>
                        <div className={styles.Panel}>
                            <div className={styles.Panel_Header}>
                                <div>
                                    <h3>Navigation</h3>
                                </div>
                            </div>
                            <div className={styles.Panel_Body}>
                                <Menu
                                    mode="inline"
                                    style={{ width: '100%' }}
                                    onClick={this.handleMenuChange}
                                    defaultSelectedKeys={['1']}
                                    defaultOpenKeys={['sub1']}
                                  >
                                    <SubMenu key="sub1" title={<span><Icon type="mail" /><span>General Information</span></span>}>
                                      <Menu.Item key="1">Website Structure</Menu.Item>
                                      <Menu.Item key="2">Date & Time</Menu.Item>
                                      <Menu.Item key="3">Candidate</Menu.Item>
                                      <Menu.Item key="4">Client</Menu.Item>
                                      <Menu.Item key="5">Jobs</Menu.Item>
                                    </SubMenu>

                                    <SubMenu key="sub2" title={<span><Icon type="mail" /><span>Chatbots</span></span>}>
                                      <Menu.Item key="6">Creating your Chatbot</Menu.Item>
                                      <Menu.Item key="7">Data</Menu.Item>
                                      <Menu.Item key="8">Candidates from Chatbot</Menu.Item>
                                      <Menu.Item key="9">Clients from Chatbot</Menu.Item>
                                      <Menu.Item key="10">Templates</Menu.Item>
                                    </SubMenu>

                                  </Menu>
                            </div>
                        </div>
                    </div>

                    <div style={{margin: 5, width: '73%'}}>
                        <div className={styles.Panel}>
                            <div className={styles.Panel_Header}>
                                <div>
                                    <h3>Information</h3>
                                </div>
                            </div>
                            <div className={styles.Panel_Body}>

                                <Tabs defaultActiveKey="1" activeKey={this.state.currentKey} tabBarStyle={{display:"none"}}>
                                    <TabPane key="1">
                                        <p>
                                            As a platform, we have divided Admin Panel into three multiple sections which allow for the ease of accessibility.
                                            <ul>
                                                <li>Dashboard</li>
                                                <li>Assistants</li>
                                                <li>Account</li>
                                            </ul>
                                            Dashboard: The Dashboard is mainly there to help give you an easily accessible toolbox which provides you with all the platform's features.<br /><br />
                                            Assistants: The Assistant's page is where you will be able to control all their Chatbots and control their operations.<br /><br />
                                            Account: The Account's page can be used to make changes to your account and control your details.
                                        </p>
                                    </TabPane>

                                    <TabPane key="2">
                                        <p>
                                            TheSearchBase uses Greenwich Mean Time (GMT) to track the time. All your automatic notifications will be based on this time and the time in which data has been collected will also be measured using this format.
                                        </p>
                                    </TabPane>

                                    <TabPane key="3">
                                        <p>
                                            Your account will be provided with a default database for the candidates which you process and collect data from. All of the data which you collect will be can be easily accessed by clicking on the Chatbot's dropdown menu and selecting 'Candidates'. This page will present you with all the candidates which have interacted with the chatbot and entered their data.
                                        </p>
                                    </TabPane>

                                    <TabPane key="4">
                                        <p>
                                            Your account will be provided with a default database for the clients which you start interacting with. This database will store all the key information which you can share with candidates.
                                        </p>
                                    </TabPane>

                                    <TabPane key="5">
                                        <p>
                                            The Jobs database is the primary location for storing all your job information. This database can be linked to your CRM and automatically import all your jobs.
                                        </p>
                                    </TabPane>

                                    <TabPane key="6">
                                        <p>
                                            To create a chatbot, you can choose to use the templates provide or create your own customised conversation flow. To create a Chatbot, you should first click on 'Assistants'. Once the page has loaded, at the top right click on 'Add Assistant'.<br />
                                            <br />
                                            You should then:<br />
                                            <ul>
                                                <li>Give your Assistant a name</li>
                                                <li>A welcome message</li>
                                                <li>A title (this will appear at the top of the chatbot)</li>
                                                <li>How long before it automatically opens a conversation (switch off if you wish to keep it silent)</li>
                                                <li>A template (if you wish to create it from a template)</li>
                                            </ul>
                                            After you have entered the necessary information, click the 'Add' button on the bottom right to save your assistant.<br />
                                            To help speed things up, a set of default values and databases will be created for your assistant. You can change the settings at any point by clicking the 'Crank' icon on your Assistant card. You can start to customise your conversation and make it more personal by clicking on the 'Flow' icon located next to the Settings icon.<br />
                                        </p>
                                    </TabPane>

                                    <TabPane key="7">
                                        If you wish to use your Assistant for specific task, such as showing candidates job opportunities, or showing clients candidate profiles then you can very easily connect your live data to the chatbot.<br /><br />
                                        To connect your available jobs to the Assistant, proceed to opening the drop-down menu of the Assistant and heading to 'Jobs'. In the middle-top of the page, click on 'Add Jobs'. You can give this group of jobs a name such as 'Jobs-Feb-2019' and select how you will provide the job data.<br />
                                        You can directly connect your CRM to our platform if you CRM provider is listed below:<br />
                                        <ul>
                                            <li>Bullhorn</li>
                                            <li>Vincere</li>
                                        </ul>
                                        Or you can upload a file from CRM providers such as:<br />
                                        <ul>
                                            <li>RDB Pro Net (Access Group)</li>
                                            <li>Mercury Xrm</li>
                                            <li>Bullhorn</li>
                                            <li>Vincere</li>
                                        </ul>
                                        Processing your jobs will take up to five seconds, and once we have processed the file, you will be able to use the data in automated conversations with candidates.<br />
                                    </TabPane>

                                    <TabPane key="8">
                                        <p>
                                            For every Assistant you create, you will have the option to connect this to a specific database. If direct CRM integration is enabled, you will then have the option to transit this data back into your CRM.<br />
                                            <br />
                                            <h4>Candidate Conversations</h4>
                                            All the conversations held with candidates and the data collected from the conversations will be held in the candidate database. Every new entry into the database will be classified as a 'new candidate', therefore from the questions asked, a profile will be made for the candidate.<br />
                                            <h4>Jobs</h4>
                                            In some cases, you may wish to start conversations with candidates, showcasing with jobs they may be interested in. In this instance, you will have the option to connect your 'Jobs' database to the chatbot.<br />
                                        </p>
                                    </TabPane>

                                    <TabPane key="9">
                                        <p>
                                            Our assistants also enable clients to directly communicate with your company and share their details, but also view undisclosed candidate profiles.<br />
                                            <br />
                                            <h4>Client Conversations</h4>
                                            Every conversation held with clients will be recorded and safely stored in a database. To give make it easier to identify a client, we build a profile for every conversation held with the assistant. By viewing a client's profile, you will able to view all their details.<br />
                                        </p>
                                    </TabPane>

                                    <TabPane key="10">
                                        <p>
                                            We have multiple starting points for recruiters to start their conversations from. When creating a chatbot, you can simply choose if you wish to start with a template.<br />
                                            <br />
                                            <h4>Template Formats</h4>
                                            We have several template formats that are best suited for certain environments.
                                            <ul>
                                                <li>General Front-website</li>
                                                <li>Specific Front-Website</li>
                                                <li>Joining Us</li>
                                                <li>Re-recruiting old clients</li>
                                                <li>Candidate experience</li>
                                                <li>Pre-screening confirmation</li>
                                                <li>Candidates with clients</li>
                                            </ul>
                                            <br />
                                            <h4>Template Conversations</h4>
                                            All the templates have been pre-made to give recruiters to save time in making them. You can at any point, change the format of the conversation and make it as personal and unique as you like.<br />
                                            <br />
                                            <h4>Collecting Feedback</h4>
                                            As a recruiter, you will have the option to collect feedback after you have placed a candidate with a client. We've tried to make this as easy for you as possible.<br />
                                            Using our pre-made templates, you can simply assign a chatbot link directly to a candidate and see what they think of their new role. You can also use similar chatbot's to ask your clients what they think of the candidate which you have recruited.<br />
                                        </p>
                                    </TabPane>

                                </Tabs>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Documentation