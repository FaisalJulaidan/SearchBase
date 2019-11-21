import React from 'react'
import {Icon, Typography, Menu, Modal} from 'antd';
import {CRMAutoPilotActions} from "store/actions";
import {Breadcrumb} from 'antd';
import 'types/TimeSlots_Types'
import {history} from "helpers";

import styles from '../Assistant/AutoPilot.module.less';

const {Title, Paragraph} = Typography;

class CRMAutoPilot extends React.Component {

    render() {
      console.log(this.props)
      const { crmAP } = this.props
      console.log(crmAP)

      return(
      <div className={styles.Header}>
          <div style={{marginBottom: 20}}>
              <Breadcrumb>
                  <Breadcrumb.Item>
                      <a href={'javascript:void(0);'}
                          onClick={() => history.push('/dashboard/auto_pilots/crm')}>
                          CRM Auto Pilots
                      </a>
                  </Breadcrumb.Item>
                  <Breadcrumb.Item>{crmAP.Name}</Breadcrumb.Item>
              </Breadcrumb>
          </div>
          <div className={styles.Title}>
              <Title>{crmAP.Name}</Title>
              <Paragraph type="secondary">
                  {crmAP.Description}
              </Paragraph>
          </div>
      </div>)
    }
}


export default CRMAutoPilot;

