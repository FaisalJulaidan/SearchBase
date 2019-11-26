import React from 'react';
import {connect} from 'react-redux';
import styles from './AutoPilot.module.less';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel';
import {
    Breadcrumb, Button, Col, Collapse, Divider, Form, Input, InputNumber, Modal, Row, Spin, Switch, Typography,
    Select, Icon, Radio
} from 'antd';
import 'types/TimeSlots_Types';
import './AutoPilot.less';
import {history} from 'helpers';
import {autoPilotActions, appointmentAllocationTimeActions} from 'store/actions';
import {campaignActions} from "store/actions"; //TODO: To be removed (Fetching assistants for referral for now)
// import CKEditor from '@ckeditor/ckeditor5-react';
import CKEditor from 'components/CKeditor/CKEditor'
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import {trimText} from "../../../../helpers";

const {Panel} = Collapse;
const ButtonGroup = Button.Group;
const FormItem = Form.Item;
const confirm = Modal.confirm;

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

const customPanelStyle = {
    borderRadius: 4,
    marginBottom: 24,
    border: 0,
    overflow: 'hidden'
};

class AssistantAutoPilot extends React.Component {
  
    state = {
        rejectApplications: false,
        acceptApplications: false,
        referApplications: false,
        contractFollowUp: false,
        sendAcceptanceEmail: false,
        sendRejectionEmail: false,
        sendReferralEmail: false,
        sendContractFollowUpEmail: false,
        sendAcceptanceSMS: false,
        sendRejectionSMS: false,
        sendReferralSMS: false,
        sendContractFollowUpSMS: false,
        sendCandidatesAppointments: false,

        acceptanceScore: null,
        acceptanceEmailBody: '<p>Congrats you got accepted.</p>',
        acceptanceSMSBody: 'Congrats you got accepted.',

        rejectionScore: null,
        rejectionEmailBody: '<p>Sorry you are not accepted.</p>',
        rejectionSMSBody: 'Sorry you are not accepted.',

        referralAssistant: null,
        referralEmailBody: '<p></p>',
        referralSMSBody: '',

        contractFollowUpSchedule: null,
        contractFollowUpEmailBody: '<p></p>',
        contractFollowUpSMSBody: '',

        sendAcceptanceEmailErrors: false,
        sendAcceptanceSMSErrors: false,
        sendRejectionEmailErrors: false,
        sendRejectionSMSErrors: false,
        sendReferralEmailErrors: false,
        sendReferralSMSErrors: false,
        sendContractFollowUpEmailErrors: false,
        sendContractFollowUpSMSErrors: false

    };

    componentDidMount() {
      console.log("mount")
        this.props.dispatch(appointmentAllocationTimeActions.fetchAAT());
        this.props.dispatch(campaignActions.fetchCampaigns()); //TODO: To be removed (Fetching assistants for referral for now)
        this.props.dispatch(autoPilotActions.fetchAutoPilot(this.props.match.params.id))
            .then(() => {
                const {autoPilot} = this.props;
                this.setState({  //TODO:: Uncomment referral fields when server-side is done
                    rejectApplications: autoPilot.RejectApplications,
                    acceptApplications: autoPilot.AcceptApplications,
                    // referApplications: autoPilot.ReferApplications,
                    // contractFollowUp: autoPilot.contractFollowUp,
                    sendAcceptanceEmail: autoPilot.SendAcceptanceEmail,
                    sendRejectionEmail: autoPilot.SendRejectionEmail,
                    // sendReferralEmail: autoPilot.SendReferralEmail,
                    // sendContractFollowUpEmail: autoPilot.SendContractFollowUpEmail,
                    sendAcceptanceSMS: autoPilot.SendAcceptanceSMS,
                    sendRejectionSMS: autoPilot.SendRejectionSMS,
                    // sendReferralSMS: autoPilot.SendReferralSMS,
                    // sendContractFollowUpSMS: autoPilot.SendContractFollowUpSMS,
                    sendCandidatesAppointments: autoPilot.SendCandidatesAppointments,
                    acceptanceScore: autoPilot.AcceptanceScore * 100,
                    acceptanceEmailBody: autoPilot.AcceptanceEmailBody,
                    acceptanceSMSBody: autoPilot.AcceptanceSMSBody.split('\n').map(x => `<p>${x ? x : '&nbsp;'}</p>`).join(' '),
                    rejectionScore: autoPilot.RejectionScore * 100,
                    rejectionEmailBody: autoPilot.RejectionEmailBody,
                    rejectionSMSBody: autoPilot.RejectionSMSBody.split('\n').map(x => `<p>${x ? x : '&nbsp;'}</p>`).join(' '),
                    // referralAssistant: autoPilot.ReferralAssistant,
                    // referralEmailBody: autoPilot.ReferralEmailBody,
                    // referralSMSBody: autoPilot.ReferralSMSBody.split('\n').map(x => `<p>${x ? x : '&nbsp;'}</p>`).join(' ')
                    // contractFollowUpSchedule: autoPilot.ContractFollowUpSchedule,
                    // contractFollowUpEmailBody: autoPilot.ContractFollowUpEmailBody,
                    // contractFollowUpSMSBody: autoPilot.ContractFollowUpSMSBody.split('\n').map(x => `<p>${x ? x : '&nbsp;'}</p>`).join(' '),
                });
            }).catch((e) => {console.log("kek"); console.log(e)})  ;
    }

    onRejectChange = (checked) => this.setState({
        rejectApplications: checked,
        sendRejectionEmail: checked ? this.state.sendRejectionEmail : false,
        sendRejectionSMS: checked ? this.state.sendRejectionSMS : false
    });
    onAcceptChange = (checked) => this.setState({
        acceptApplications: checked,
        sendAcceptanceEmail: checked ? this.state.sendAcceptanceEmail : false,
        sendAcceptanceSMS: checked ? this.state.sendAcceptanceSMS : false
    });
    onReferChange = (checked) => this.setState({
        referApplications: checked,
        sendReferralEmail: checked ? this.state.sendReferralEmail : false,
        sendReferralSMS: checked ? this.state.sendReferralSMS : false
    });
    onContractFollowUpChange = (checked) => this.setState({
        contractFollowUp: checked,
        sendContractFollowUpEmail: checked ? this.state.sendContractFollowUpEmail : false,
        sendContractFollowUpSMS: checked ? this.state.sendContractFollowUpSMS : false
    });
    onSendAcceptanceEmailChange = (checked) => this.setState({sendAcceptanceEmail: checked});
    onSendRejectionEmailChange = (checked) => this.setState({sendRejectionEmail: checked});
    onSendReferralEmailChange = (checked) => this.setState({sendReferralEmail: checked});
    onSendContractFollowUpEmailChange = (checked) => this.setState({sendContractFollowUpEmail: checked});
    onSendAcceptanceSMSChange = (checked) => this.setState({sendAcceptanceSMS: checked});
    onSendRejectionSMSChange = (checked) => this.setState({sendRejectionSMS: checked});
    onSendReferralSMSChange = (checked) => this.setState({sendReferralSMS: checked});
    onSendContractFollowUpSMSChange = (checked) => this.setState({sendContractFollowUpSMS: checked});

    handleDelete = () => {
        confirm({
            title: `Delete auto pilot confirmation`,
            content: `If you click OK, this auto pilot will be deleted and disconnected from all assistants that are connected to it`,
            onOk: () => {
                this.props.dispatch(autoPilotActions.deleteAutoPilot(this.props.autoPilot.ID))
                    .then(() => history.push('/dashboard/auto_pilots'));
            }
        });
    };

    onActivateHandler = (checked) => {
        if (!checked) {
            confirm({
                title: `Deactivate auto pilot`,
                content: <p>Are you sure you want to deactivate this auto pilot</p>,
                onOk: () => {
                    this.props.dispatch(autoPilotActions.updateStatus(checked, this.props.autoPilot.ID));
                }
            });
            return;
        }
        this.props.dispatch(autoPilotActions.updateStatus(checked, this.props.autoPilot.ID));
    };

    onSubmit = () => this.props.form.validateFields((err, values) => {
        console.log(err);
        if (!err) {
            const /**@type AutoPilot*/ autoPilot = this.props.autoPilot || {};
            const {state, TimeSlotsRef} = this;
            // const timeSlots = TimeSlotsRef.current.state.weekDays;
            let payload = {
                active: autoPilot.Active,
                name: values.name,
                description: values.description,

                acceptApplications: state.acceptApplications,
                rejectApplications: state.rejectApplications,
                referApplications: state.referApplications,
                contractFollowUp: state.contractFollowUp,

                acceptanceScore: state.acceptanceScore / 100,
                rejectionScore: state.rejectionScore / 100,
                referralAssistant: state.referralAssistant,
                contractFollowUpSchedule: state.contractFollowUpSchedule,

                sendAcceptanceEmail: state.sendAcceptanceEmail,
                acceptanceEmailTitle: values.acceptanceEmailTitle || autoPilot.AcceptanceEmailTitle,
                acceptanceEmailBody: state.acceptanceEmailBody,

                sendAcceptanceSMS: state.sendAcceptanceSMS,
                acceptanceSMSBody: state.acceptanceSMSBody.replace(/<\/p>/g, '\n').replace(/<p>/g, '').replace(/&nbsp;/g, ''),

                sendRejectionEmail: state.sendRejectionEmail,
                rejectionEmailTitle: values.rejectionEmailTitle || autoPilot.RejectionEmailTitle,
                rejectionEmailBody: state.rejectionEmailBody,

                sendRejectionSMS: state.sendRejectionSMS,
                rejectionSMSBody: state.rejectionSMSBody.replace(/<\/p>/g, '\n').replace(/<p>/g, '').replace(/&nbsp;/g, ''),

                sendReferralEmail: state.sendReferralEmail,
                sendReferralEmailTitle: values.referralEmailTitle || autoPilot.ReferralEmailTitle,
                referralEmailBody: state.referralEmailBody,

                sendReferralSMS: state.sendReferralSMS,
                referralSMSBody: state.referralSMSBody.replace(/<\/p>/g, '\n').replace(/<p>/g, '').replace(/&nbsp;/g, ''),

                sendContractFollowUpEmail: state.sendContractFollowUpEmail,
                sendContractFollowUpEmailTitle: values.contractFollowUpEmailTitle || autoPilot.ContractFollowUpEmailTitle,
                contractFollowUpEmailBody: state.contractFollowUpEmailBody,

                sendContractFollowUpSMS: state.sendContractFollowUpSMS,
                contractFollowUpSMSBody: state.contractFollowUpSMSBody.replace(/<\/p>/g, '\n').replace(/<p>/g, '').replace(/&nbsp;/g, ''),

                appointmentAllocationTimes: values.AppointmentAllocationTimes,
                sendCandidatesAppointments: state.sendCandidatesAppointments
            };
            if (payload.sendAcceptanceEmail) {
                if (!payload.acceptanceEmailTitle || !payload.acceptanceEmailBody)
                    return this.setState({sendAcceptanceEmailErrors: true});
                else
                    this.setState({sendAcceptanceEmailErrors: false});
            } else
                this.setState({sendAcceptanceEmailErrors: false});

            if (payload.sendAcceptanceSMS) {
                if (!payload.acceptanceSMSBody)
                    return this.setState({sendAcceptanceSMSErrors: true});
                else
                    this.setState({sendAcceptanceSMSErrors: false});
            } else
                this.setState({sendAcceptanceSMSErrors: false});

            if (payload.sendRejectionEmail) {
                if (!payload.rejectionEmailTitle || !payload.rejectionEmailBody)
                    return this.setState({sendRejectionEmailErrors: true});
                else
                    this.setState({sendRejectionEmailErrors: false});
            } else
                this.setState({sendRejectionEmailErrors: false});

            if (payload.sendRejectionSMS) {
                if (!payload.rejectionSMSBody)
                    return this.setState({sendRejectionSMSErrors: true});
                else
                    this.setState({sendRejectionSMSErrors: false});
            } else
                this.setState({sendRejectionSMSErrors: false});

            if (payload.sendReferralEmail) {
                if (!payload.referralEmailTitle || !payload.referralEmailBody)
                    return this.setState({sendReferralEmailErrors: true});
                else
                    this.setState({sendReferralEmailErrors: false});
            } else
                this.setState({sendReferralEmailErrors: false});

            if (payload.sendReferralSMS) {
                if (!payload.referralSMSBody)
                    return this.setState({sendReferralSMSErrors: true});
                else
                    this.setState({sendReferralSMSErrors: false});
            } else
                this.setState({sendReferralSMSErrors: false});

            if (payload.sendContractFollowUpEmail) {
                if (!payload.contractFollowUpEmailTitle || !payload.contractFollowUpEmailBody)
                    return this.setState({sendContractFollowUpEmailErrors: true});
                else
                    this.setState({sendContractFollowUpEmailErrors: false});
            } else
                this.setState({sendContractFollowUpEmailErrors: false});

            if (payload.sendContractFollowUpSMS) {
                if (!payload.contractFollowUpSMSBody)
                    return this.setState({sendContractFollowUpSMSErrors: true});
                else
                    this.setState({sendContractFollowUpSMSErrors: false});
            } else
                this.setState({sendContractFollowUpSMSErrors: false});


            payload.appointmentAllocationTimes = payload.appointmentAllocationTimes === 'You have no timetables, please create one!' ? null : payload.appointmentAllocationTimes;
            console.log(payload);
            this.props.dispatch(autoPilotActions.updateAutoPilotConfigs(autoPilot.ID, payload));
        }

    });


    render() {
        const /**@type AutoPilot*/ autoPilot = this.props.autoPilot;
        const layout = {
            labelCol: {span: 4},
            wrapperCol: {span: 18}
        };
        const {getFieldDecorator} = this.props.form;

        return (
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <div style={{marginBottom: 20}}>
                            <Breadcrumb>
                                <Breadcrumb.Item>
                                    <a href={'javascript:void(0);'}
                                       onClick={() => history.push('/dashboard/auto_pilots/assistant')}>
                                        Auto Pilots
                                    </a>
                                </Breadcrumb.Item>
                                <Breadcrumb.Item>{autoPilot?.Name}</Breadcrumb.Item>
                            </Breadcrumb>
                        </div>

                        <Row>
                            <Col span={20}>
                                <Title>{autoPilot?.Name}</Title>
                                <Paragraph type="secondary">
                                    {autoPilot?.Description}
                                </Paragraph>
                            </Col>
                            <Col span={4}>
                                <Switch checkedChildren="On" unCheckedChildren="Off"
                                        checked={autoPilot?.Active}
                                        loading={this.props.isStatusChanging}
                                        onChange={this.onActivateHandler}
                                        style={{ marginTop: '17%', marginLeft: '70%' }}/>
                            </Col>
                        </Row>
                    </div>

                    <div className={styles.Body}>
                        {!autoPilot || this.props.aatLoading ? <Spin/> :
                            <Form layout='vertical' wrapperCol={{span: 15}} style={{width: '100%'}}
                                  id={'AutoPilotForm'}>
                                <FormItem label="Name">
                                    {getFieldDecorator('Name', {
                                        initialValue: autoPilot.Name,
                                        rules: [
                                            {
                                                whitespace: true,
                                                required: true,
                                                message: 'Enter a name for your auto pilot'
                                            },
                                            {
                                                validator: (_, value, callback) => {
                                                    // check if the value equals any of the name from
                                                    // this.props.autoPilotsSlots
                                                    // if there is an error return the callback with the message
                                                    if (this.props.autoPilotsList?.some(autoPilot => autoPilot.Name === value
                                                        && this.props.autoPilot.Name !== value))  
                                                        return callback(value + ' is duplicated');
                                                    else
                                                        return callback();
                                                }
                                            }
                                        ]
                                    })(
                                        <Input placeholder="Auto Pilot Name"/>
                                    )}
                                </FormItem>

                                <FormItem label="Description">
                                    {getFieldDecorator('description', {
                                        initialValue: autoPilot?.Description,
                                        rules: [{}]
                                    })(
                                        <Input placeholder="Auto Pilot Description"/>
                                    )}
                                </FormItem>

                                <Divider/>

                                <Collapse bordered={false}>
                                    <Panel header={<h2> Applications Acceptance Automation</h2>} key="1"
                                           style={customPanelStyle}>
                                        <FormItem label="Auto accept applicants "
                                                  help="Select the percentage to auto accept the applicants">
                                            {getFieldDecorator('AcceptApplications', {
                                                valuePropName: 'checked', 
                                                setFieldsValue: this.state.acceptApplications
                                            })(
                                                <>
                                                    <Switch onChange={this.onAcceptChange}
                                                            style={{marginRight: 15}}
                                                    />
                                                    A score greater than
                                                    <InputNumber min={0} max={100}
                                                                 onChange={value => this.setState({acceptanceScore: value})}
                                                                 value={this.state.acceptanceScore}
                                                                 key={autoPilot?.AcceptanceScore ? 'notLoadedYet' : 'loaded'}
                                                                 formatter={value => `${value}%`}
                                                                 style={{marginLeft: 15}}
                                                                 disabled={!this.state.acceptApplications}/>
                                                </>
                                            )}
                                        </FormItem>

                                        <FormItem label="Auto send acceptance emails"
                                                  help="Accepted applicants will be notified via email if email is provided in the chat  (candidates applications only)"
                                        >
                                            {getFieldDecorator('sendAcceptanceEmail', {
                                                initialValue: autoPilot?.SendAcceptanceEmail,
                                                rules: []
                                            })(
                                                <div style={{marginLeft: 3}}>
                                                    <Switch onChange={this.onSendAcceptanceEmailChange}
                                                            checked={this.state.sendAcceptanceEmail}
                                                            disabled={!this.state.acceptApplications}

                                                    />
                                                </div>
                                            )}
                                        </FormItem>

                                        {
                                            this.state.sendAcceptanceEmail &&
                                            <FormItem label="Acceptance Email Title" vi>
                                                {getFieldDecorator('acceptanceEmailTitle', {
                                                    initialValue: autoPilot?.AcceptanceEmailTitle,
                                                    rules: [{required: true}]
                                                })(
                                                    <Input placeholder="Congrats you got accepted"/>
                                                )}
                                            </FormItem>
                                        }

                                        {
                                            this.state.sendAcceptanceEmail &&
                                            <Row className={styles.CEKwrapper}>
                                                <h4>Acceptance letter</h4>

                                                {
                                                    this.state.sendAcceptanceEmailErrors &&
                                                    <p style={{color: 'red'}}> * Title and Body field are requierd</p>
                                                }

                                                <ButtonGroup style={{margin: '5px 0'}}>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                acceptanceEmailBody: this.state.acceptanceEmailBody + ' ${candidateName}$'
                                                            })
                                                        }>
                                                        Candidate Name
                                                    </Button>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                acceptanceEmailBody: this.state.acceptanceEmailBody + ' ${candidateEmail}$'
                                                            })
                                                        }>
                                                        Candidate Email
                                                    </Button>
                                                </ButtonGroup>

                                                <Row>
                                                    <Col span={15}>
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{toolbar: toolbar}}
                                                            data={this.state.acceptanceEmailBody}
                                                            onChange={(event, editor) => this.setState(state => state.acceptanceEmailBody = editor?.getData())}
                                                            onInit={editor => this.setState(state => state.acceptanceEmailBody = editor?.getData())}
                                                        />
                                                    </Col>
                                                </Row>
                                            </Row>
                                        }

                                        <FormItem label="Auto send SMS"
                                                  help="Accepted applicants will be notified via SMS if telephone number is provided in the chat  (candidates applications only)">
                                            {getFieldDecorator('sendAcceptanceSMS', {
                                                initialValue: autoPilot?.SendAcceptanceSMS,
                                                rules: []
                                            })(
                                                <div style={{marginLeft: 3}}>
                                                    <Switch onChange={this.onSendAcceptanceSMSChange}
                                                            checked={this.state.sendAcceptanceSMS}
                                                            disabled={!this.state.acceptApplications}/>

                                                </div>
                                            )}
                                        </FormItem>

                                        {
                                            this.state.sendAcceptanceSMS &&
                                            <Row className={styles.CEKwrapper}>
                                                <h4>Acceptance message</h4>
                                                {
                                                    this.state.sendAcceptanceSMSErrors &&
                                                    <p style={{color: 'red'}}> * Body field is required</p>
                                                }
                                                <ButtonGroup style={{margin: '5px 0'}}>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                acceptanceSMSBody: this.state.acceptanceSMSBody + ' ${candidateName}$'
                                                            })
                                                        }>
                                                        Candidate Name
                                                    </Button>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                acceptanceSMSBody: this.state.acceptanceSMSBody + ' ${candidateEmail}$'
                                                            })
                                                        }>
                                                        Candidate Email
                                                    </Button>
                                                </ButtonGroup>

                                                <Row>
                                                    <Col span={15}>
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{toolbar: ['undo', 'redo']}}
                                                            data={this.state.acceptanceSMSBody}
                                                            onChange={(event, editor) => this.setState(state => state.acceptanceSMSBody = editor?.getData())}
                                                            onInit={editor => this.setState(state => state.acceptanceSMSBody = editor?.getData())}
                                                        />
                                                    </Col>
                                                </Row>
                                            </Row>
                                        }
                                    </Panel>

                                    <Panel header={<h2> Applications Rejection Automation</h2>} key="2"
                                           style={customPanelStyle}>
                                        <Form.Item label="Auto reject applicants "
                                                   help="Select the percentage to auto reject the applicants">
                                            {getFieldDecorator('rejectApplications', {
                                                valuePropName: 'checked'
                                            })(
                                                <>
                                                    <Switch onChange={this.onRejectChange} style={{marginRight: 15}}
                                                            checked={this.state.rejectApplications}/>
                                                    A score less than
                                                    <InputNumber min={1} max={100}
                                                                 onChange={value => this.setState({rejectionScore: value})}
                                                                 formatter={value => `${value}%`}
                                                                 key={autoPilot?.RejectionScore ? 'notLoadedYet' : 'loaded'}
                                                                 value={this.state.rejectionScore}
                                                                 style={{marginLeft: 15}}
                                                                 disabled={!this.state.rejectApplications}/>
                                                </>
                                            )}
                                        </Form.Item>

                                        <FormItem label="Auto send rejection email"
                                                  help="Rejected applicants will be notified via email if email is provided in the chat (candidates applications only)">
                                            {getFieldDecorator('SendRejectionEmail', {
                                                initialValue: autoPilot.SendRejectionEmail,
                                                rules: []
                                            })(
                                                <div style={{marginLeft: 3}}>
                                                    <Switch onChange={this.onSendRejectionEmailChange}
                                                            checked={this.state.sendRejectionEmail}
                                                            disabled={!this.state.rejectApplications}/>
                                                </div>
                                            )}
                                        </FormItem>

                                        { this.state.sendRejectionEmail &&
                                            <FormItem label="Rejection Email Title">
                                                {getFieldDecorator('RejectionEmailTitle', {
                                                    initialValue: autoPilot?.RejectionEmailTitle,
                                                    rules: [{required: true}]
                                                })(
                                                    <Input placeholder="Sorry you got rejected"/>
                                                )}
                                            </FormItem>
                                        }
                                        { this.state.sendRejectionEmail &&
                                            <Row className={styles.CEKwrapper}>
                                              <FormItem label="Rejection Letter">
                                                <ButtonGroup style={{margin: '5px 0px'}}>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                rejectionEmailBody: this.state.rejectionEmailBody + ' ${candidateName}$'
                                                            })
                                                        }>
                                                        Candidate Name
                                                    </Button>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                rejectionEmailBody: this.state.rejectionEmailBody + ' ${candidateEmail}$'
                                                            })
                                                        }>
                                                        Candidate Email
                                                    </Button>
                                                </ButtonGroup>
                                                <Row>
                                                    <Col span={15}>
                                                    {getFieldDecorator('RejectionEmailBody', {
                                                        initialValue: autoPilot?.RejectionEmailBody,
                                                        rules: [{required: true}]
                                                    })(
                                                        <CKEditor
                                                                editor={ClassicEditor}
                                                                config={{toolbar: toolbar}}/>
                                                    )}
                                                    </Col>
                                                </Row>
                                            </FormItem>
                                            </Row>
                                        }

                                        <FormItem label="Auto send rejection SMS"
                                                  help="Rejected applicants will be notified via SMS if telephone number is provided in the chat  (candidates applications only)">
                                            {getFieldDecorator('SendRejectionSMS', {
                                                initialValue: autoPilot.SendRejectionSMS,
                                                rules: []
                                            })(
                                                <div style={{marginLeft: 3}}>
                                                    <Switch onChange={this.onSendRejectionSMSChange}
                                                            disabled={!this.state.rejectApplications}/>
                                                </div>
                                            )}
                                        </FormItem>

                                        { this.state.sendRejectionSMS &&
                                            <Row className={styles.CEKwrapper}>
                                              <FormItem label="Rejection Letter">
                                                <ButtonGroup style={{margin: '5px 0px'}}>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                rejectionSMSBody: this.state.rejectionSMSBody + ' ${candidateName}$'
                                                            })
                                                        }>
                                                        Candidate Name
                                                    </Button>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                rejectionSMSBody: this.state.rejectionSMSBody + ' ${candidateEmail}$'
                                                            })
                                                        }>
                                                        Candidate Email
                                                    </Button>
                                                </ButtonGroup>
                                                <Row>
                                                    <Col span={15}>
                                                    {getFieldDecorator('RejectionEmailBody', {
                                                        initialValue: autoPilot?.RejectionEmailBody,
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
                                <Divider/>
                                <h2>Contract Follow Up</h2>
                                <Collapse bordered={false}>
                                    <Panel header={<h2>Automatically suggests contract roles</h2>} key="4"
                                           style={customPanelStyle}>

                                        <FormItem label="Send job suggestion (before their role finishes)">
                                            {getFieldDecorator('contractFollowUp', {
                                                valuePropName: 'checked'
                                            })(
                                                <Switch onChange={this.onContractFollowUpChange}
                                                        style={{marginRight: 15}}
                                                        checked={this.state.contractFollowUp}
                                                />
                                            )}
                                            {getFieldDecorator("contractFollowUpSchedule", {initialValue: "2"})(
                                                <Radio.Group  disabled={!this.state.contractFollowUp}>
                                                    <Radio.Button value="1">1 Week</Radio.Button>
                                                    <Radio.Button value="2">2 Weeks</Radio.Button>
                                                    <Radio.Button value="3">3 Weeks</Radio.Button>
                                                </Radio.Group>
                                            )}
                                        </FormItem>

                                        <FormItem label="Auto send Email"
                                                  help="Applicants will be notified via email if email is provided in the chat  (candidates applications only)"
                                        >
                                            {getFieldDecorator('sendContractFollowUpEmail', {
                                                initialValue: autoPilot?.SendContractFollowUpEmail,
                                                rules: []
                                            })(
                                                <div style={{marginLeft: 3}}>
                                                    <Switch onChange={this.onSendContractFollowUpEmailChange}
                                                            checked={this.state.sendContractFollowUpEmail}
                                                            disabled={!this.state.contractFollowUp}

                                                    />
                                                </div>
                                            )}
                                        </FormItem>

                                        {
                                            this.state.sendContractFollowUpEmail &&
                                            <FormItem label="Role Suggestion Email Title" vi>
                                                {getFieldDecorator('contractFollowUpEmailTitle', {
                                                    initialValue: autoPilot?.ContractFollowUpEmailTitle,
                                                    rules: [{required: true}]
                                                })(
                                                    <Input placeholder=""/>
                                                )}
                                            </FormItem>
                                        }

                                        {
                                            this.state.sendContractFollowUpEmail &&
                                            <Row className={styles.CEKwrapper}>
                                                <h4>Role Suggestion letter</h4>

                                                {
                                                    this.state.sendContractFollowUpEmailErrors &&
                                                    <p style={{color: 'red'}}> * Title and Body field are required</p>
                                                }

                                                <ButtonGroup style={{margin: '5px 0'}}>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                contractFollowUpEmailBody: this.state.contractFollowUpEmailBody + ' ${candidateName}$'
                                                            })
                                                        }>
                                                        Candidate Name
                                                    </Button>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                contractFollowUpEmailBody: this.state.contractFollowUpEmailBody + ' ${candidateEmail}$'
                                                            })
                                                        }>
                                                        Candidate Email
                                                    </Button>
                                                </ButtonGroup>

                                                <Row>
                                                    <Col span={15}>
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{toolbar: toolbar}}
                                                            data={this.state.contractFollowUpEmailBody}
                                                            onChange={(event, editor) => this.setState(state => state.contractFollowUpEmailBody = editor?.getData())}
                                                            onInit={editor => this.setState(state => state.contractFollowUpEmailBody = editor?.getData())}
                                                        />
                                                    </Col>
                                                </Row>
                                            </Row>
                                        }

                                        <FormItem label="Auto send SMS"
                                                  help="Applicants will be notified via SMS if telephone number is provided in the chat  (candidates applications only)">
                                            {getFieldDecorator('sendContractFollowUpSMS', {
                                                initialValue: autoPilot?.SendContractFollowUpSMS,
                                                rules: []
                                            })(
                                                <div style={{marginLeft: 3}}>
                                                    <Switch onChange={this.onSendContractFollowUpSMSChange}
                                                            checked={this.state.sendContractFollowUpSMS}
                                                            disabled={!this.state.contractFollowUp}/>

                                                </div>
                                            )}
                                        </FormItem>

                                        {
                                            this.state.sendContractFollowUpSMS &&
                                            <Row className={styles.CEKwrapper}>
                                                <h4>Role suggestion message</h4>
                                                {
                                                    this.state.sendContractFollowUpSMSErrors &&
                                                    <p style={{color: 'red'}}> * Body field is required</p>
                                                }
                                                <ButtonGroup style={{margin: '5px 0'}}>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                contractFollowUpSMSBody: this.state.contractFollowUpSMSBody + ' ${candidateName}$'
                                                            })
                                                        }>
                                                        Candidate Name
                                                    </Button>
                                                    <Button
                                                        onClick={() =>
                                                            this.setState({
                                                                contractFollowUpSMSBody: this.state.contractFollowUpSMSBody + ' ${candidateEmail}$'
                                                            })
                                                        }>
                                                        Candidate Email
                                                    </Button>
                                                </ButtonGroup>

                                                <Row>
                                                    <Col span={15}>
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{toolbar: ['undo', 'redo']}}
                                                            data={this.state.contractFollowUpSMSBody}
                                                            onChange={(event, editor) => this.setState(state => state.contractFollowUpSMSBody = editor?.getData())}
                                                            onInit={editor => this.setState(state => state.contractFollowUpSMSBody = editor?.getData())}
                                                        />
                                                    </Col>
                                                </Row>
                                            </Row>
                                        }

                                    </Panel>
                                </Collapse>

                                <Divider/>
                                <h2> Manage Appointments Automation</h2>
                                <FormItem label="Auto manage and send candidates appointments"
                                          help="Accepted candidates will receive an email (if provided) to pick
                                           a time slot for an appointment. You can then confirm these
                                           appointments from the Appointments page"

                                >
                                    {getFieldDecorator('sendCandidatesAppointments', {
                                        initialValue: autoPilot.SendCandidatesAppointments,
                                        rules: []
                                    })(
                                        <div style={{marginLeft: 3}}>
                                            <Switch
                                                onChange={(value) => this.setState({sendCandidatesAppointments: value})}
                                                checked={this.state.sendCandidatesAppointments}/>
                                        </div>
                                    )}
                                </FormItem>
                                <Form.Item
                                    label="Time table"
                                    help="Select a time table to be used for automatic appointment slots generation">
                                    {getFieldDecorator('AppointmentAllocationTimes', {
                                        initialValue: this.props.autoPilot?.AppointmentAllocationTimeID,
                                        rules: [{
                                            required: this.state.sendCandidatesAppointments,
                                            message: 'Select a time table '
                                        }]
                                    })(
                                        <Select
                                            disabled={!this.state.sendCandidatesAppointments}
                                            dropdownRender={menu => (
                                                <div>
                                                    {menu}
                                                    <Divider style={{margin: '4px 0'}}/>
                                                    <div
                                                        onMouseDown={() => history.push(`/dashboard/appointments?tab=TimeSlots`)}
                                                        style={{padding: '8px', cursor: 'pointer'}}>
                                                        <Icon type="plus"/> Create time table
                                                    </div>
                                                </div>
                                            )}>
                                            {this.props.appointmentAllocationTime.map((time, i) => {
                                                return (
                                                    <Select.Option key={i} value={time.ID}>{time.Name}</Select.Option>);
                                            })}
                                        </Select>
                                    )}

                                </Form.Item>
                            </Form>
                        }


                        <Button type={'primary'} size={'large'} onClick={this.onSubmit}
                                style={{marginTop: 30}}>
                            Save changes
                        </Button>

                        <Divider/>
                        <Button type={'danger'} size={'large'} onClick={this.handleDelete}>Delete Auto Pilot</Button>


                        {/*Blur Effect (Hidden) */}
                        <div style={{display: 'none'}}>
                            <svg id="svg-filter">
                                <filter id="svg-blur">
                                    <feGaussianBlur in="SourceGraphic" stdDeviation="2"></feGaussianBlur>
                                </filter>
                            </svg>
                        </div>

                    </div>
            </NoHeaderPanel>
            
        );
    }
}

function mapStateToProps(state) {
    return {
        autoPilot: state.autoPilot.autoPilot,
        autoPilotsList: state.autoPilot.autoPilotsList,
        isLoading: state.autoPilot.isLoading,
        isStatusChanging: state.autoPilot.isStatusChanging,
        appointmentAllocationTime: state.appointmentAllocationTime.allocationTimes,
        aatLoading: state.appointmentAllocationTime.isLoading,
        campaignOptions: state.campaign.campaignOptions //TODO: To be removed (Fetching assistants for referral for now)
    };
}

export default connect(mapStateToProps)(Form.create()(AssistantAutoPilot));
