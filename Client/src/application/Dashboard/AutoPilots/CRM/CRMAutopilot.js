import React from 'react'
import {connect} from 'react-redux';
import {Breadcrumb, Button, Col, Collapse, Form, Input, Divider, Row, Switch, Typography, Select, Modal} from 'antd';
import CKEditor from 'components/CKeditor/CKEditor'
// Client\src\components\CKeditor\CKEditor.js
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import 'types/TimeSlots_Types'
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {history, trimText} from "helpers";

import {CRMAutoPilotActions} from "store/actions";

import styles from '../Assistant/AutoPilot.module.less';

const {Panel} = Collapse;
const ButtonGroup = Button.Group;
const FormItem = Form.Item;
const {confirm} = Modal

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
      sendReferralEmail: this.props?.crmAP?.SendReferralEmail,
      sendReferralSMS: this.props?.crmAP?.SendReferralSMS,
      autoRefer: !(this.props?.crmAP?.ReferralAssistantID === undefined || this.props?.crmAP?.ReferralAssistantID === null)
    }

    componentWillMount() {
      this.props.dispatch(CRMAutoPilotActions.fetchCRMAutoPilot(this.props.match.params.id))
    }

    onActivateHandler = (checked) => {
        if (!checked) {
            confirm({
                title: `Deactivate CRM Autopilot`,
                content: <p>Are you sure you want to deactivate this CRM Autopilot</p>,
                onOk: () => {
                    this.props.dispatch(CRMAutoPilotActions.updateStatus(this.props.match.params.id, checked));
                }
            });
            return;
        }
        this.props.dispatch(CRMAutoPilotActions.updateStatus(this.props.match.params.id, checked));
    };

    onSubmit = ()  =>  {
      this.props.form.validateFields((err, values) => {
        if(!err){
          this.props.dispatch(CRMAutoPilotActions.updateCRMAutoPilotConfigs(this.props.crmAP.ID, values))
        }
      })
    }

    render() {
      const {getFieldDecorator} = this.props.form;  
      const { crmAP } = this.props
      const { sendReferralEmail, sendReferralSMS, autoRefer } = this.state
      let activeKeys = []


      
      activeKeys = autoRefer ? [...activeKeys, "1"] : activeKeys
      return(
      <NoHeaderPanel>
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
        </div>
        <div className={styles.Body}>
            <div className={styles.Title}>
                <Row>
                    <Col span={20}>
                        <Title>{crmAP?.Name}</Title>
                        <Paragraph type="secondary">
                            {crmAP?.Description}
                        </Paragraph>
                    </Col>
                    <Col span={4}>
                        <Switch checkedChildren="On" unCheckedChildren="Off"
                                checked={crmAP?.Active}
                                loading={this.props.isStatusChanging}
                                onChange={this.onActivateHandler}
                                style={{ marginTop: '17%', marginLeft: '70%' }}/>
                    </Col>
                </Row>
            </div>
            { crmAP &&
                <Form layout='vertical' wrapperCol={{span: 15}} style={{width: '100%'}} id={'CRMAutoPilotForm'}>
                    <h2>General</h2>
                    <FormItem label="Name">
                      {getFieldDecorator('Name', {
                          initialValue: crmAP.Name,
                          rules: [{required: true}]
                      })(
                          <Input placeholder="CRM Autopilot name"/>
                      )}
                    </FormItem>
                    <FormItem label="Description">
                      {getFieldDecorator('Description', {
                          initialValue: crmAP.Description,
                          rules: [{required: true}]
                      })(
                          <Input placeholder="CRM Autopilot description"/>
                      )}
                    </FormItem>

                    <h2>Referral</h2>
                    <Collapse bordered={false} defaultActiveKey={activeKeys}>
                        <Panel header={<h2>Automatically asks candidates for referral after placement</h2>}
                                key="1"
                                style={customPanelStyle}>
                            <FormItem label="Auto refer applicants "
                                      help="Select an assistant to auto refer the applicants">
                                <Switch onChange={e => this.setState({autoRefer: e})} style={{marginRight: 15}} defaultChecked={this.state.autoRefer}/>
                            </FormItem>
                            {this.state.autoRefer &&
                              <>
                                <FormItem label={"Assistant"}>
                                    {getFieldDecorator("ReferralAssistantID", {
                                        initialValue: crmAP.ReferralAssistantID,
                                        rules: [{
                                            required: true,
                                            message: "Please select an assistant"
                                        }],
                                    })(
                                        <Select placeholder={"Please select an assistant"}
                                                loading={this.props.isLoading}
                                                disabled={!this.state.autoRefer}>
                                            {(() => {
                                                return this.props?.assistants.map((item, key) => {
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
                                    {getFieldDecorator('SendReferralEmail', {
                                        initialValue: sendReferralEmail,
                                    })(
                                        <div style={{marginLeft: 3}}>
                                            <Switch checked={sendReferralEmail} onChange={e => this.setState({sendReferralEmail: e})}/>
                                        </div>
                                    )}
                                </FormItem>
                              </>
                            }
                            <>
                                <FormItem label="Referral Email Title" style={sendReferralEmail && this.state.autoRefer ? {} : {display: 'none'}}>
                                  {getFieldDecorator('ReferralEmailTitle', {
                                        initialValue: crmAP.ReferralEmailTitle,
                                        rules: [{required: true}],
                                        hidden: !sendReferralEmail,
                                    })(
                                         <Input placeholder="referral email title"/>
                                    )}
                                 
                                </FormItem>
                                <Row className={styles.CEKwrapper} style={sendReferralEmail && this.state.autoRefer ? {} : {display: 'none'}}>                                    
                                    <FormItem label="Referral Email Body">
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
                                            {getFieldDecorator('ReferralEmailBody', {
                                                hidden: !sendReferralEmail,
                                                rules: [{required: true}],
                                                initialValue: crmAP.ReferralEmailBody
                                            })(
                                                <CKEditor editor={ClassicEditor} >
    
                                                </CKEditor>
                                            )}
                                          </Col>
                                      </Row>
                                    </FormItem>
                                </Row>
                            </>
                            { this.state.autoRefer &&
                            <FormItem label="Auto send SMS"
                                      help="Referred applicants will be notified via SMS if telephone number is provided in the chat  (candidates applications only)">
                                {getFieldDecorator('SendReferralSMS', {
                                    initialValue: sendReferralSMS,
                                    rules: []
                                })(
                                    <div style={{marginLeft: 3}}>
                                        <Switch checked={sendReferralSMS} onChange={e => this.setState({sendReferralSMS: e})}/>
                                    </div>
                                )}
                            </FormItem>
                            }
                            { sendReferralSMS &&
                            <Row className={styles.CEKwrapper}>
                                <FormItem label="Referral SMS Body">
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
                                        {getFieldDecorator('ReferralSMSBody', {
                                            initialValue: crmAP.ReferralSMSBody,
                                            hidden: !sendReferralSMS,
                                            rules: [{required: true}]
                                        })(
                                          <CKEditor
                                              editor={ClassicEditor}
                                              config={{toolbar: ['undo', 'redo']}}/>
                                        )}
                                      </Col>
                                  </Row>
                                </FormItem>
                            </Row>
                            }
                        </Panel>
                    </Collapse>
                    <Button type={'primary'} size={'large'} onClick={this.onSubmit} style={{marginTop: 30}}>
                        Save changes
                    </Button>
                    <Divider/>
                    <Button type={'danger'} size={'large'} onClick={this.handleDelete}>Delete Auto Pilot</Button>
                </Form> }
        </div>
      </NoHeaderPanel>)
    }
}



function mapStateToProps(state) {
    return {
        isLoading: state.CRMAutoPilot.isLoading,
        assistants: state.assistant.assistantList,
        crmAP: state.CRMAutoPilot.CRMAutoPilot
    };
}

export default connect(mapStateToProps)(Form.create()(CRMAutoPilot));

