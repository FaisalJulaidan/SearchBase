import React from 'react';
import { connect } from 'react-redux';
import { Breadcrumb, Button, Col, Collapse, Form, Input, Divider, Row, Switch, Typography, Select, Modal } from 'antd';
import CKEditor from 'components/CKeditor/CKEditor';
import LoadingSpinner from 'components/LoadingSpinner/LoadingSpinner';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import 'types/TimeSlots_Types';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel';
import { history, trimText } from 'helpers';

import { CRMAutoPilotActions } from 'store/actions';

import styles from '../Assistant/AutoPilot.module.less';

const { Panel } = Collapse;
const ButtonGroup = Button.Group;
const FormItem = Form.Item;
const { confirm } = Modal;

const customPanelStyle = {
    // borderRadius: 4,
    // marginBottom: 24,
    // border: 0,
    // overflow: 'hidden'
};

const { Title, Paragraph } = Typography;

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
        autoRefer: this.props?.crmAP?.AutoReferApplicants
    };

    componentWillMount() {
        this.props.dispatch(CRMAutoPilotActions.fetchCRMAutoPilot(this.props.match.params.id));
    }

    componentWillReceiveProps(){
      console.log(this.props)
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

    setFormKV = (key, value) => this.props.form.setFieldsValue({ [key]: value });
    appendFormKV = (key, value) => this.props.form.setFieldsValue({ [key]: `${this.props.form.getFieldValue(key)}${value}` });

    onSubmit = () => {
        this.props.form.validateFields((err, values) => {
            console.log(values);
            if (!err) {
                this.props.dispatch(CRMAutoPilotActions.updateCRMAutoPilotConfigs(this.props.crmAP.ID, { ...this.props.crmAP, ...values }));
            }
        });
    };

    componentDidUpdate(){
      if(this.state.autoRefer !== this.props.form.getFieldValue('AutoReferApplicants')){
        this.setState({autoRefer: this.props.form.getFieldValue('AutoReferApplicants')})
      }
    }

    render() {
        const { getFieldDecorator, getFieldValue } = this.props.form;
        const crmAP = this.props.crmAP ? this.props.crmAP : {}
        const { autoRefer } = this.state;
        let activeKeys = [];
        activeKeys = autoRefer ? [...activeKeys, '1'] : activeKeys;
        return (
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <div style={{ marginBottom: 20 }}>
                            <Breadcrumb>
                                <Breadcrumb.Item>
                                    <a href={'javascript:void(0);'}
                                       onClick={() => history.push('/dashboard/auto_pilots/crm')}>
                                        CRM Auto Pilots
                                    </a>
                                </Breadcrumb.Item>
                                <Breadcrumb.Item>{crmAP?.Name}</Breadcrumb.Item>
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
                        {crmAP &&
                        <Form layout='vertical' wrapperCol={{ span: 15 }} style={{ width: '100%' }}
                              id={'CRMAutoPilotForm'}>
                            <h2>General</h2>
                            <FormItem label="Name">
                                {getFieldDecorator('Name', {
                                    initialValue: crmAP.Name,
                                    rules: [{ required: true }]
                                })(
                                    <Input placeholder="CRM Autopilot name"/>
                                )}
                            </FormItem>
                            <FormItem label="Description">
                                {getFieldDecorator('Description', {
                                    initialValue: crmAP.Description,
                                    rules: [{ required: false }]
                                })(
                                    <Input placeholder="CRM Autopilot description"/>
                                )}
                            </FormItem>

                            <Divider/>
                            <h2>Referral</h2>
                            <Collapse defaultActiveKey={activeKeys}>
                                <Panel header={<h3>Automatically asks candidates for referral after placement</h3>}
                                       key="1"
                                       style={customPanelStyle}>
                                    <FormItem label="Auto refer applicants "
                                              extra="Auto refer the applicants to an assistant">
                                        {getFieldDecorator('AutoReferApplicants', {
                                            initialValue: crmAP.AutoReferApplicants,
                                            valuePropName: 'checked'
                                        })(
                                            <Switch onChange={e => this.setState({ autoRefer: e })}
                                                    style={{ marginRight: 15 }}/>
                                        )}
                                    </FormItem>
                                    {this.state.autoRefer &&
                                    <>
                                        <FormItem label={'Assistant'}
                                                  extra="Select an assistant to auto refer the applicants">
                                            {getFieldDecorator('ReferralAssistantID', {
                                                initialValue: crmAP.ReferralAssistantID,
                                                rules: [{
                                                    required: true,
                                                    message: 'Please select an assistant'
                                                }]
                                            })(
                                                <Select placeholder={'Please select an assistant'}
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
                                                  extra="Referred applicants will be notified via email if email is provided in the chat  (candidates applications only)">
                                            {getFieldDecorator('SendReferralEmail', {
                                                initialValue: crmAP.SendReferralEmail,
                                                valuePropName: 'checked'
                                            })(
                                                  <Switch/>
                                            )}
                                        </FormItem>
                                    </>
                                    }
                                    {getFieldValue('SendReferralEmail') && this.state.autoRefer &&
                                    <>
                                        <FormItem label="Referral Email Title">
                                            {getFieldDecorator('ReferralEmailTitle', {
                                                initialValue: crmAP.ReferralEmailTitle,
                                                rules: [{ required: true }],
                                                hidden: !(getFieldValue('SendReferralEmail') && this.state.autoRefer),
                                            })(
                                                <Input placeholder="referral email title"/>
                                            )}

                                        </FormItem>
                                        <Row className={styles.CEKwrapper}
                                             style={getFieldValue(`SendReferralEmail`) && this.state.autoRefer ? {} : { display: 'none' }}>
                                            <FormItem label="Referral Email Body">
                                                <ButtonGroup style={{ margin: '5px 0' }}>
                                                    <Button
                                                        onClick={() => this.appendFormKV('ReferralEmailBody', ' ${assistantLink}$')}>
                                                        Assistant Link
                                                    </Button>
                                                </ButtonGroup>
                                                <Row>
                                                    <Col span={15}>
                                                        {getFieldDecorator('ReferralEmailBody', {
                                                            hidden: !(getFieldValue('SendReferralEmail') && this.state.autoRefer),
                                                            rules: [{ required: true }],
                                                            initialValue: crmAP.ReferralEmailBody
                                                        })(
                                                            <CKEditor editor={ClassicEditor}
                                                                      config={{ toolbar: toolbar }}/>
                                                        )}
                                                    </Col>
                                                </Row>
                                            </FormItem>
                                        </Row>
                                    </>}
                                    {this.state.autoRefer &&
                                    <FormItem label="Auto send SMS"
                                              extra="Referred applicants will be notified via SMS if telephone number is provided in the chat  (candidates applications only)">
                                        {getFieldDecorator('SendReferralSMS', {
                                            initialValue: crmAP.SendReferralSMS,
                                            rules: [],
                                            valuePropName: 'checked'
                                        })(
                                            <Switch/>
                                        )}
                                    </FormItem>
                                    }
                                    {getFieldValue('SendReferralSMS') && this.state.autoRefer &&
                                    <Row className={styles.CEKwrapper}>
                                        <FormItem label="Referral SMS Body">
                                            <ButtonGroup style={{ margin: '5px 0' }}>
                                                <Button
                                                    onClick={() => this.appendFormKV('ReferralSMSBody', ' ${assistantLink}$')}>
                                                    Assistant Link
                                                </Button>
                                            </ButtonGroup>
                                            <Row>
                                                <Col span={15}>
                                                    {getFieldDecorator('ReferralSMSBody', {
                                                        initialValue: crmAP.ReferralSMSBody,
                                                        hidden: !(getFieldValue('SendReferralSMS') && this.state.autoRefer),
                                                        rules: [{ required: true }]
                                                    })(
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{ toolbar: ['undo', 'redo'] }}/>
                                                    )}
                                                </Col>
                                            </Row>
                                        </FormItem>
                                    </Row>}
                                </Panel>
                            </Collapse>
                            <Button type={'primary'} size={'large'} onClick={this.onSubmit} style={{ marginTop: 30 }}>
                                Save changes
                            </Button>
                            <Divider/>
                            <Button type={'danger'} size={'large'} onClick={this.handleDelete}>Delete Auto
                                Pilot</Button>
                        </Form>}
                    </div>
                </NoHeaderPanel>);
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

