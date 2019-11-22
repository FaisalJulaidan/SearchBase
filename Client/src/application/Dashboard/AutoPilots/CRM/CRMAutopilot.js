import React from 'react'
import {Breadcrumb, Button, Col, Collapse, Form, Input, Row, Switch, Typography} from 'antd';
import CKEditor from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import 'types/TimeSlots_Types'
import {history} from "helpers";

import {CRMAutoPilotActions} from "store/actions";

import styles from '../Assistant/AutoPilot.module.less';

const {Panel} = Collapse;
const ButtonGroup = Button.Group;
const FormItem = Form.Item;

const customPanelStyle = {
    borderRadius: 4,
    marginBottom: 24,
    border: 0,
    overflow: 'hidden'
};

const {Title, Paragraph} = Typography;

const toolbar = [
    'heading',
    'bold',
    'italic',
    'link',
    'bulletedList',
    'numberedList',
    'undo',
    'redo'
];

class CRMAutoPilot extends React.Component {

    state = {
      referralEmailBody: this.props.crmAP.referralEmailBody,
      sendReferralEmail: this.props.crmAP.referralEmailBody && this.props.crmAP.ReferralEmailTitle,
      sendReferralSMS: this.props.crmAP.referralSMSBody && this.props.crmAP.ReferralSMS,
      referralSMSBody: this.props.crmAP.referralSMSBody
    }

    render() {
      console.log(this.props)
      const {getFieldDecorator} = this.props.form;  
      const { crmAP } = this.props
      const { sendReferralEmail, sendReferralSMS } = this.state

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
          <div className={styles.Body}>
              <Form layout='vertical' wrapperCol={{span: 15}} style={{width: '100%'}} id={'CRMAutoPilotForm'}>
                  <h2>Referral</h2>
                  <Collapse bordered={false}>
                      <Panel header={<h2>Automatically asks candidates for referral after placement</h2>}
                              key="3"
                              style={customPanelStyle}>
                          <FormItem label="Auto refer applicants "
                                    help="Select an assistant to auto refer the applicants">
                              {getFieldDecorator('referApplications', {
                                  valuePropName: 'checked',
                                  initialValue: crmAP.LastReferral !== null,
                              })(
                                  <Switch onChange={this.onReferChange}
                                          style={{marginRight: 15}}
                                  />
                              )}
                          </FormItem>
                          <FormItem label={"Assistant"}>
                              {getFieldDecorator("referralAssistant", {
                                  initialValue: crmAP.referralAssistantID,
                                  rules: [{
                                      required: true,
                                      message: "Please select an assistant"
                                  }],
                              })(
                                  <Select placeholder={"Please select an assistant"}
                                          loading={this.props.isLoading}
                                          disabled={!this.state.referApplications}>
                                      {(() => {
                                          return this.props.campaignOptions?.assistants?.map((item, key) => {
                                              return (
                                                  <Select.Option key={key} value={item.ID}>
                                                      {trimText.capitalize(trimText.trimDash(item.Name))}
                                                  </Select.Option>
                                              );
                                          });
                                      })()}
                                  </Select>
                              )}
                          </FormItem>
                          <FormItem label="Auto send referral emails"
                                    help="Referred applicants will be notified via email if email is provided in the chat  (candidates applications only)">
                              {getFieldDecorator('sendReferralEmail', {
                                  initialValue: sendReferralEmail
                              })(
                                  <div style={{marginLeft: 3}}>
                                      <Switch onChange={e => this.setState({sendReferralEmail: e})}/>
                                  </div>
                              )}
                          </FormItem>
                          <FormItem label="Referral Email Title" vi>
                              {getFieldDecorator('referralEmailTitle', {
                                  initialValue: crmAP.ReferralEmailTitle,
                                  rules: [{required: true}]
                              })(
                                  <Input placeholder=""/>
                              )}
                          </FormItem>
                          { sendReferralEmail &&
                              <Row className={styles.CEKwrapper}>
                                  <h4>Referral letter</h4>
                                  { this.state.sendReferralEmailErrors &&
                                    <p style={{color: 'red'}}> * Title and Body field are required</p>}
                                  <ButtonGroup style={{margin: '5px 0'}}>
                                      <Button onClick={() => this.setState({ referralEmailBody: this.state.referralEmailBody + ' ${candidateName}$' })}>
                                          Candidate Name
                                      </Button>
                                      <Button onClick={() => this.setState({ referralEmailBody: this.state.referralEmailBody + ' ${candidateEmail}$' })}>
                                          Candidate Email
                                      </Button>
                                  </ButtonGroup>
                                  <Row>
                                      <Col span={15}>
                                          <CKEditor
                                              editor={ClassicEditor}
                                              config={{toolbar: toolbar}}
                                              data={this.state.referralEmailBody}
                                              onChange={(event, editor) => this.setState(state => state.referralEmailBody = editor?.getData())}
                                              onInit={editor => this.setState(state => state.referralEmailBody = editor?.getData())}
                                          />
                                      </Col>
                                  </Row>
                              </Row>
                          }
                          <FormItem label="Auto send SMS"
                                    help="Referred applicants will be notified via SMS if telephone number is provided in the chat  (candidates applications only)">
                              {getFieldDecorator('sendReferralSMS', {
                                  initialValue: sendReferralSMS,
                                  rules: []
                              })(
                                  <div style={{marginLeft: 3}}>
                                      <Switch onChange={e => this.setState({sendReferralSMS: e})}/>
                                  </div>
                              )}
                          </FormItem>
                          {sendReferralSMS &&
                              <Row className={styles.CEKwrapper}>
                                  <h4>Referral message</h4>
                                  {this.state.sendReferralSMSErrors &&
                                      <p style={{color: 'red'}}> * Body field is required</p>}
                                  <ButtonGroup style={{margin: '5px 0'}}>
                                      <Button onClick={() =>this.setState({ referralSMSBody: this.state.referralSMSBody + ' ${candidateName}$'})}>
                                          Candidate Name
                                      </Button>
                                      <Button onClick={() => this.setState({referralSMSBody: this.state.referralSMSBody + ' ${candidateEmail}$'})}>
                                          Candidate Email
                                      </Button>
                                  </ButtonGroup>

                                  <Row>
                                      <Col span={15}>
                                          <CKEditor
                                              editor={ClassicEditor}
                                              config={{toolbar: ['undo', 'redo']}}
                                              data={this.state.referralSMSBody}
                                              onChange={(event, editor) => this.setState(state => state.referralSMSBody = editor?.getData())}
                                              onInit={editor => this.setState(state => state.referralSMSBody = editor?.getData())}
                                          />
                                      </Col>
                                  </Row>
                              </Row>
                          }

                      </Panel>
                  </Collapse>
              </Form> 
          </div>
      </div>)
    }
}


export default Form.create()(CRMAutoPilot);

