import React from 'react';
import { connect } from 'react-redux';
import styles from './AutoPilot.module.less';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel';
import {
    Breadcrumb,
    Button,
    Col,
    Collapse,
    Divider,
    Form,
    Input,
    InputNumber,
    Modal,
    Row,
    Spin,
    Switch,
    Typography,
    Select,
    Icon,
} from 'antd';
import 'types/TimeSlots_Types';
import './AutoPilot.less';
import { history } from 'helpers';
import { autoPilotActions, appointmentAllocationTimeActions } from 'store/actions';
import CKEditor from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

const { Panel } = Collapse;
const ButtonGroup = Button.Group;
const FormItem = Form.Item;
const confirm = Modal.confirm;

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

const customPanelStyle = {
    borderRadius: 4,
    marginBottom: 24,
    border: 0,
    overflow: 'hidden'
};

class AutoPilot extends React.Component {

    state = {
        rejectApplications: false,
        acceptApplications: false,
        sendAcceptanceEmail: false,
        sendRejectionEmail: false,
        sendAcceptanceSMS: false,
        sendRejectionSMS: false,
        sendCandidatesAppointments: false,
        acceptanceScore: null,
        acceptanceEmailBody: '<p>Congrats you got accepted.</p>',
        acceptanceSMSBody: 'Congrats you got accepted.',

        rejectionScore: null,
        rejectionEmailBody: '<p>Sorry you are not accepted.</p>',
        rejectionSMSBody: 'Sorry you are not accepted.',

        sendAcceptanceEmailErrors: false,
        sendAcceptanceSMSErrors: false,
        sendRejectionEmailErrors: false,
        sendRejectionSMSErrors: false

    };

    componentDidMount() {
        this.props.dispatch(appointmentAllocationTimeActions.fetchAAT());
        this.props.dispatch(autoPilotActions.fetchAutoPilot(this.props.match.params.id))
            .then(() => {
                const { autoPilot } = this.props;
                this.setState({
                    rejectApplications: autoPilot.RejectApplications,
                    acceptApplications: autoPilot.AcceptApplications,
                    sendAcceptanceEmail: autoPilot.SendAcceptanceEmail,
                    sendRejectionEmail: autoPilot.SendRejectionEmail,
                    sendAcceptanceSMS: autoPilot.SendAcceptanceSMS,
                    sendRejectionSMS: autoPilot.SendRejectionSMS,
                    sendCandidatesAppointments: autoPilot.SendCandidatesAppointments,
                    acceptanceScore: autoPilot.AcceptanceScore * 100,
                    acceptanceEmailBody: autoPilot.AcceptanceEmailBody,
                    acceptanceSMSBody: autoPilot.AcceptanceSMSBody.split('\n').map(x => `<p>${x ? x : '&nbsp;'}</p>`).join(' '),
                    rejectionScore: autoPilot.RejectionScore * 100,
                    rejectionEmailBody: autoPilot.RejectionEmailBody,
                    rejectionSMSBody: autoPilot.RejectionSMSBody.split('\n').map(x => `<p>${x ? x : '&nbsp;'}</p>`).join(' ')
                });
            }).catch(() => history.push(`/dashboard/auto_pilots`));
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
    onSendAcceptanceEmailChange = (checked) => this.setState({ sendAcceptanceEmail: checked });
    onSendRejectionEmailChange = (checked) => this.setState({ sendRejectionEmail: checked });
    onSendAcceptanceSMSChange = (checked) => this.setState({ sendAcceptanceSMS: checked });
    onSendRejectionSMSChange = (checked) => this.setState({ sendRejectionSMS: checked });

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

    onSubmit = () => this.props.form.validateFields((err, values) => {
        console.log(err);
        if (!err) {
            const /**@type AutoPilot*/ autoPilot = this.props.autoPilot || {};
            const { state, TimeSlotsRef } = this;
            // const timeSlots = TimeSlotsRef.current.state.weekDays;
            let payload = {
                active: autoPilot.Active,
                name: values.name,
                description: values.description,

                acceptApplications: state.acceptApplications,
                rejectApplications: state.rejectApplications,

                acceptanceScore: state.acceptanceScore / 100,
                rejectionScore: state.rejectionScore / 100,

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

                appointmentAllocationTimes: values.AppointmentAllocationTimes,
                sendCandidatesAppointments: state.sendCandidatesAppointments
            };
            if (payload.sendAcceptanceEmail) {
                if (!payload.acceptanceEmailTitle || !payload.acceptanceEmailBody)
                    return this.setState({ sendAcceptanceEmailErrors: true });
                else
                    this.setState({ sendAcceptanceEmailErrors: false });
            } else
                this.setState({ sendAcceptanceEmailErrors: false });

            if (payload.sendAcceptanceSMS) {
                if (!payload.acceptanceSMSBody)
                    return this.setState({ sendAcceptanceSMSErrors: true });
                else
                    this.setState({ sendAcceptanceSMSErrors: false });
            } else
                this.setState({ sendAcceptanceSMSErrors: false });

            if (payload.sendRejectionEmail) {
                if (!payload.rejectionEmailTitle || !payload.rejectionEmailBody)
                    return this.setState({ sendRejectionEmailErrors: true });
                else
                    this.setState({ sendRejectionEmailErrors: false });
            } else
                this.setState({ sendRejectionEmailErrors: false });

            if (payload.sendRejectionSMS) {
                if (!payload.rejectionSMSBody)
                    return this.setState({ sendRejectionSMSErrors: true });
                else
                    this.setState({ sendRejectionSMSErrors: false });
            } else
                this.setState({ sendRejectionSMSErrors: false });

            payload.appointmentAllocationTimes = payload.appointmentAllocationTimes === 'You have no timetables, please create one!' ? null : payload.appointmentAllocationTimes;
            console.log(payload);
            this.props.dispatch(autoPilotActions.updateAutoPilotConfigs(autoPilot.ID, payload));
        }

    });


    render() {
        const /**@type AutoPilot*/ autoPilot = this.props.autoPilot;
        const layout = {
            labelCol: { span: 4 },
            wrapperCol: { span: 18 }
        };
        const { getFieldDecorator } = this.props.form;

        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <div style={{ marginBottom: 20 }}>
                            <Breadcrumb>
                                <Breadcrumb.Item>
                                    <a href={'javascript:void(0);'}
                                       onClick={() => history.push('/dashboard/auto_pilots')}>
                                        Auto Pilots
                                    </a>
                                </Breadcrumb.Item>
                                <Breadcrumb.Item>{autoPilot?.Name}</Breadcrumb.Item>
                            </Breadcrumb>
                        </div>

                        <div className={styles.Title}>
                            <Title>{autoPilot?.Name}</Title>
                            <Paragraph type="secondary">
                                {autoPilot?.Description}
                            </Paragraph>
                        </div>
                    </div>

                    <div className={styles.Body}>
                        {!autoPilot || this.props.aatLoading ? <Spin/> :
                            <Form layout='vertical' wrapperCol={{ span: 15 }} style={{ width: '100%' }}
                                  id={'AutoPilotForm'}>
                                <FormItem label="Name">
                                    {getFieldDecorator('name', {
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
                                            {getFieldDecorator('acceptApplications', {
                                                valuePropName: 'checked'
                                            })(
                                                <>
                                                    <Switch onChange={this.onAcceptChange}
                                                            style={{ marginRight: 15 }}
                                                            checked={this.state.acceptApplications}
                                                    />
                                                    A score greater than
                                                    <InputNumber min={0} max={100}
                                                                 onChange={value => this.setState({ acceptanceScore: value })}
                                                                 value={this.state.acceptanceScore}
                                                                 key={autoPilot?.AcceptanceScore ? 'notLoadedYet' : 'loaded'}
                                                                 formatter={value => `${value}%`}
                                                                 style={{ marginLeft: 15 }}
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
                                                <div style={{ marginLeft: 3 }}>
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
                                                    rules: [{ required: true }]
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
                                                    <p style={{ color: 'red' }}> * Title and Body field are requierd</p>
                                                }

                                                <ButtonGroup style={{ margin: '5px 0' }}>
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
                                                            config={{ toolbar: toolbar }}
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
                                                <div style={{ marginLeft: 3 }}>
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
                                                    <p style={{ color: 'red' }}> * Body field is required</p>
                                                }
                                                <ButtonGroup style={{ margin: '5px 0' }}>
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
                                                            config={{ toolbar: ['undo', 'redo'] }}
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
                                                    <Switch onChange={this.onRejectChange} style={{ marginRight: 15 }}
                                                            checked={this.state.rejectApplications}/>
                                                    A score less than
                                                    <InputNumber min={1} max={100}
                                                                 onChange={value => this.setState({ rejectionScore: value })}
                                                                 formatter={value => `${value}%`}
                                                                 key={autoPilot?.RejectionScore ? 'notLoadedYet' : 'loaded'}
                                                                 value={this.state.rejectionScore}
                                                                 style={{ marginLeft: 15 }}
                                                                 disabled={!this.state.rejectApplications}/>
                                                </>
                                            )}
                                        </Form.Item>

                                        <FormItem label="Auto send rejection email"
                                                  help="Rejected applicants will be notified via email if email is provided in the chat (candidates applications only)">
                                            {getFieldDecorator('sendRejectionEmail', {
                                                initialValue: autoPilot.SendRejectionEmail,
                                                rules: []
                                            })(
                                                <div style={{ marginLeft: 3 }}>
                                                    <Switch onChange={this.onSendRejectionEmailChange}
                                                            checked={this.state.sendRejectionEmail}
                                                            disabled={!this.state.rejectApplications}/>
                                                </div>
                                            )}
                                        </FormItem>

                                        {
                                            this.state.sendRejectionEmail &&
                                            <FormItem label="Rejection Email Title">
                                                {getFieldDecorator('rejectionEmailTitle', {
                                                    initialValue: autoPilot?.RejectionEmailTitle,
                                                    rules: [{ required: true }]
                                                })(
                                                    <Input placeholder="Sorry you got rejected"/>
                                                )}
                                            </FormItem>
                                        }

                                        {
                                            this.state.sendRejectionEmail &&
                                            <Row className={styles.CEKwrapper}>
                                                <h4>Rejection Letter</h4>

                                                {
                                                    this.state.sendRejectionEmailErrors &&
                                                    <p style={{ color: 'red' }}> * Title and Body field are requierd</p>
                                                }

                                                <ButtonGroup style={{ margin: '5px 0px' }}>
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
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{ toolbar: toolbar }}
                                                            data={this.state.rejectionEmailBody}
                                                            onChange={(event, editor) => this.setState(state => state.rejectionEmailBody = editor?.getData())}
                                                            onInit={editor => this.setState(state => state.rejectionEmailBody = editor?.getData())}
                                                        />
                                                    </Col>
                                                </Row>
                                            </Row>
                                        }

                                        <FormItem label="Auto send rejection SMS"
                                                  help="Rejected applicants will be notified via SMS if telephone number is provided in the chat  (candidates applications only)">
                                            {getFieldDecorator('sendRejectionEmail', {
                                                initialValue: autoPilot.SendRejectionSMS,
                                                rules: []
                                            })(
                                                <div style={{ marginLeft: 3 }}>
                                                    <Switch onChange={this.onSendRejectionSMSChange}
                                                            checked={this.state.sendRejectionSMS}
                                                            disabled={!this.state.rejectApplications}/>
                                                </div>
                                            )}
                                        </FormItem>

                                        {
                                            this.state.sendRejectionSMS &&
                                            <Row className={styles.CEKwrapper}>
                                                <h4>Rejection Letter</h4>

                                                {
                                                    this.state.sendRejectionSMSErrors &&
                                                    <p style={{ color: 'red' }}> * Body field is requierd</p>
                                                }
                                                <ButtonGroup style={{ margin: '5px 0px' }}>
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
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{ toolbar: ['undo', 'redo'] }}
                                                            data={this.state.rejectionSMSBody}
                                                            onChange={(event, editor) => this.setState(state => state.rejectionSMSBody = editor?.getData())}
                                                            onInit={editor => this.setState(state => state.rejectionSMSBody = editor?.getData())}
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
                                           appointments from the Calendar page"

                                >
                                    {getFieldDecorator('sendCandidatesAppointments', {
                                        initialValue: autoPilot.SendCandidatesAppointments,
                                        rules: []
                                    })(
                                        <div style={{ marginLeft: 3 }}>
                                            <Switch onChange={(value) => this.setState({sendCandidatesAppointments: value})}
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
                                            required: true,
                                            message: 'Select a time table '
                                        }]
                                    })(
                                        <Select
                                            dropdownRender={menu => (
                                                <div>
                                                    {menu}
                                                    <Divider style={{ margin: '4px 0' }} />
                                                    <div onMouseDown={() => history.push(`/dashboard/appointments?tab=TimeSlots`)} style={{ padding: '8px', cursor: 'pointer' }}>
                                                        <Icon type="plus" /> Create time table
                                                    </div>
                                                </div>
                                            )}>
                                            {this.props.appointmentAllocationTime.map((time, i) => {
                                                return (<Select.Option key={i} value={time.ID}>{time.Name}</Select.Option>);
                                            })}
                                        </Select>
                                    )}

                                </Form.Item>
                            </Form>
                        }


                        <Button type={'primary'} size={'large'} onClick={this.onSubmit}
                                style={{ marginTop: 30 }}>
                            Save changes
                        </Button>

                        <Divider/>
                        <Button type={'danger'} size={'large'} onClick={this.handleDelete}>Delete Auto Pilot</Button>


                        {/*Blur Effect (Hidden) */}
                        <div style={{ display: 'none' }}>
                            <svg id="svg-filter">
                                <filter id="svg-blur">
                                    <feGaussianBlur in="SourceGraphic" stdDeviation="2"></feGaussianBlur>
                                </filter>
                            </svg>
                        </div>

                    </div>
                </NoHeaderPanel>
            </>
        );
    }
}

function mapStateToProps(state) {
    return {
        autoPilot: state.autoPilot.autoPilot,
        autoPilotsList: state.autoPilot.autoPilotsList,
        isLoading: state.autoPilot.isLoading,
        appointmentAllocationTime: state.appointmentAllocationTime.allocationTimes,
        aatLoading: state.appointmentAllocationTime.isLoading,
        assistantList: state.assistant.assistantList
    };
}

export default connect(mapStateToProps)(Form.create()(AutoPilot));
