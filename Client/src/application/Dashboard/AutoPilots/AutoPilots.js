import React from 'react'
import styles from "./AutoPilots.module.less";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Icon, Typography, Menu, Modal, Tabs} from 'antd';
import 'types/TimeSlots_Types'

import AssistantAutopilots from './Assistant/AssistantAutopilots'
import CRMAutopilots from './CRM/CRMAutopilots'

const {Title, Paragraph} = Typography;

class AutoPilots extends React.Component {

    // it must be an array of Menu.Item. ViewBox expect that in its options Menu
    optionsMenuItems = [
        <Menu.Item style={{padding:10, paddingRight: 30}} key="edit">
            <Icon type="edit" theme="twoTone" twoToneColor="#595959" style={{marginRight: 5}}/>
            Edit
        </Menu.Item>,
        <Menu.Item style={{padding:10, paddingRight: 30}} key="delete">
            <Icon type="delete" theme="twoTone" twoToneColor="#f50808" />
            Delete
        </Menu.Item>
    ];

    checkPageIs = (name) => {
      if(this.props.location.pathname.indexOf(name.toLowerCase()) !== -1){
        return name
      }
      return null
      }

    setTab = (tabKey) => {
      if(!this.checkPageIs(tabKey.toLowerCase())) {
        console.log(`setting to ${tabKey}`)
        let newPage = `/dashboard/auto_pilots/${tabKey.toLowerCase()}`
        this.props.history.push(newPage)
      }
    }
    componentDidMount(){
      if(!this.checkPageIs("assistant") && !this.checkPageIs("crm")){
        this.setTab("assistant")
      }
    }

    render() {      
      let def = this.checkPageIs("crm") ? "CRM" : "Assistant"
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <Title className={styles.Title}>
                            <Icon type="clock-circle"/> Auto Pilots
                        </Title>
                        <Paragraph type="secondary">
                            Connect your Assistants to an Auto Pilot to automate managing candidate acceptance and appointment scheduling
                        </Paragraph>
                    </div>
                    <Tabs onTabClick={this.setTab} defaultActiveKey={def}>
                      <Tabs.TabPane tab="Assistant Autopilots" key="Assistant">
                          <AssistantAutopilots/>
                      </Tabs.TabPane>
                      <Tabs.TabPane tab="CRM Autopilots" key="CRM">
                          <CRMAutopilots/>
                      </Tabs.TabPane>
                    </Tabs>
                </NoHeaderPanel>
            </>
        )
    }
}

export default AutoPilots