import React from 'react'
import styles from "./AutoPilots.module.less";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Icon, Typography, Menu, Modal, Tabs} from 'antd';
import 'types/TimeSlots_Types'

import AssistantAutopilots from './Assistant/AssistantAutopilots'
import CRMAutopilots from './CRM/CRMAutopilots'

const {Title, Paragraph} = Typography;

class AutoPilots extends React.Component {

    state = {
      tab: null
    }

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
      return this.props.location.pathname.indexOf(name) !== -1
    }

    setTab = (tabKey) => {
      if(!this.checkPageIs(tabKey.toLowerCase())) {
        this.setState({tab: tabKey})
        let newPage = `/dashboard/auto_pilots/${tabKey.toLowerCase()}`
        this.props.history.push(newPage)
      }
    }

    render() {
        
        let key = this.state.tab ? this.state.tab : this.checkPageIs("assistant") ? "Assistant" : "CRM"
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
                    <Tabs onTabClick={this.setTab} activeKey={key}>
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