import React from 'react';
import { connect } from 'react-redux';
import styles from './AutoPilot.module.less';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel';
import {
    Breadcrumb, Button, Col, Collapse, Divider, Form, Input, InputNumber, Modal, Row, Spin, Switch, Typography,
    Select, Icon
} from 'antd';
import 'types/TimeSlots_Types';
import './AutoPilot.less';
import { history } from 'helpers';
import { autoPilotActions, appointmentAllocationTimeActions } from 'store/actions';

import CKEditor from 'components/CKeditor/CKEditor';
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
    // borderRadius: 4,
    // marginBottom: 24,
    // border: 0,
    // overflow: 'hidden'
};

class AssistantAutoPilot extends React.Component {
    componentDidMount() {
        this.props.dispatch(appointmentAllocationTimeActions.fetchAAT());
        this.props.dispatch(autoPilotActions.fetchAutoPilot(this.props.match.params.id));
    }

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

    setFormKV = (key, value) => this.props.form.setFieldsValue({ [key]: value });
    appendFormKV = (key, value) => this.props.form.setFieldsValue({ [key]: `${this.props.form.getFieldValue(key)}${value}` });

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

    fixScores = (values) => {
        let keys = ['AcceptanceScore', 'RejectionScore'];
        Object.keys(values).filter(key => keys.includes(key)).forEach(key => values[key] = values[key] / 100);
        return values;
    };

    onSubmit = () => this.props.form.validateFields((err, values) => {
        console.log(this.props.form);
        if (!err) {
            const /**@type AutoPilot*/ autoPilot = this.props.autoPilot || {};
            values = this.fixScores(values);
            this.props.dispatch(autoPilotActions.updateAutoPilotConfigs(autoPilot.ID, { ...this.props.autoPilot, ...values }));
        }

    });

    render() {
        const /**@type AutoPilot*/ autoPilot = this.props.autoPilot;
        const { getFieldDecorator, getFieldValue } = this.props.form;

        let openCollapse1 = [autoPilot?.AcceptApplications, autoPilot?.RejectApplications];
        openCollapse1 = openCollapse1.map((val, i) => ({
            i: i + 1,
            val
        })).filter(item => item.val).map(item => item.i.toString());
        let openCollapse2 = [autoPilot?.SendCandidatesAppointments];
        openCollapse2 = openCollapse2.map((val, i) => ({
            i: i + 1,
            val
        })).filter(item => item.val).map(item => item.i.toString());

        return (
            <NoHeaderPanel panelStyles={{ position: 'relative' }}>
                <div className={styles.Header}>
                    <div style={{ marginBottom: 20 }}>
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
                        <Form layout='vertical' wrapperCol={{ span: 15 }} style={{ width: '100%' }}
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
                                {getFieldDecorator('Description', {
                                    initialValue: autoPilot?.Description,
                                    rules: [{}]
                                })(
                                    <Input placeholder="Auto Pilot Description"/>
                                )}
                            </FormItem>

                            <Divider/>
                            <h2>Qualifier</h2>
                            <Collapse defaultActiveKey={openCollapse1}>
                                <Panel header={<h3> Applications Acceptance Automation</h3>} key="1"
                                       style={customPanelStyle}>
                                    <FormItem label="Auto accept applicants "
                                              help="Select the percentage to auto accept the applicants">
                                        {getFieldDecorator('AcceptApplications', {
                                            valuePropName: 'checked',
                                            initialValue: autoPilot?.AcceptApplications
                                        })(
                                            <Switch style={{ marginRight: 15 }}/>
                                        )}
                                        A score greater than
                                        {getFieldDecorator('AcceptanceScore', {
                                            rules: [{ required: true }],
                                            hidden: !getFieldValue('AcceptApplications'),
                                            initialValue: (autoPilot?.AcceptanceScore * 100).toFixed(0)
                                        })(
                                            <InputNumber min={0} max={100}
                                                         formatter={value => `${value}%`}
                                                         style={{ marginLeft: 15 }}
                                                         disabled={!getFieldValue('AcceptApplications')}/>
                                        )}
                                    </FormItem>

                                    <FormItem label="Auto send acceptance emails"
                                              help="Accepted applicants will be notified via email if email is provided in the chat  (candidates applications only)"
                                    >
                                        {getFieldDecorator('SendAcceptanceEmail', {
                                            initialValue: autoPilot?.SendAcceptanceEmail,
                                            hidden: !getFieldValue('SendAcceptanceEmail'),
                                            valuePropName: 'checked',
                                            rules: []
                                        })(
                                            <Switch onChange={value => this.setState({ sendAcceptanceEmail: value })}
                                                    disabled={!getFieldValue('AcceptApplications')}/>
                                        )}
                                    </FormItem>

                                    {getFieldValue('SendAcceptanceEmail') &&
                                    <FormItem label="Acceptance Email Title">
                                        {getFieldDecorator('AcceptanceEmailTitle', {
                                            initialValue: autoPilot?.AcceptanceEmailTitle,
                                            hidden: !getFieldValue('SendAcceptanceEmail'),
                                            rules: [{ required: true }]
                                        })(
                                            <Input placeholder="Congrats you got accepted"/>
                                        )}
                                    </FormItem>}

                                    {getFieldValue('SendAcceptanceEmail') &&
                                    <Row className={styles.CEKwrapper}>
                                        <FormItem label="Acceptance Letter">
                                            <ButtonGroup style={{ margin: '5px 0' }}>
                                                <Button
                                                    onClick={() => this.appendFormKV('AcceptanceEmailBody', ' ${candidateName}$')}>
                                                    Candidate Name
                                                </Button>
                                                <Button
                                                    onClick={() => this.appendFormKV('AcceptanceEmailBody', ' ${candidateEmail}$')}>
                                                    Candidate Email
                                                </Button>
                                            </ButtonGroup>
                                            <Row>
                                                <Col span={15}>
                                                    {getFieldDecorator('AcceptanceEmailBody', {
                                                        initialValue: autoPilot?.AcceptanceEmailBody,
                                                        hidden: !getFieldValue('SendAcceptanceEmail'),
                                                        rules: [{ required: true }]
                                                    })(
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{ toolbar: toolbar }}/>
                                                    )}
                                                </Col>
                                            </Row>
                                        </FormItem>
                                    </Row>
                                    }

                                    <FormItem label="Auto send SMS"
                                              help="Accepted applicants will be notified via SMS if telephone number is provided in the chat  (candidates applications only)">
                                        {getFieldDecorator('SendAcceptanceSMS', {
                                            initialValue: autoPilot?.SendAcceptanceSMS,
                                            valuePropName: 'checked',
                                            rules: []
                                        })(
                                            <Switch disabled={!getFieldValue('AcceptApplications')}/>
                                        )}
                                    </FormItem>

                                    {getFieldValue('SendAcceptanceSMS') &&
                                    <Row className={styles.CEKwrapper}>
                                        <FormItem label="Acceptance Letter">
                                            <ButtonGroup style={{ margin: '5px 0' }}>
                                                <Button
                                                    onClick={() => this.appendFormKV('AcceptanceSMSBody', ' ${candidateName}$')}>
                                                    Candidate Name
                                                </Button>
                                                <Button
                                                    onClick={() => this.appendFormKV('AcceptanceSMSBody', ' ${candidateEmail}$')}>
                                                    Candidate Email
                                                </Button>
                                            </ButtonGroup>
                                            <Row>
                                                <Col span={15}>
                                                    {getFieldDecorator('AcceptanceSMSBody', {
                                                        initialValue: autoPilot?.AcceptanceSMSBody,
                                                        hidden: !getFieldValue('SendAcceptanceSMS'),
                                                        rules: [{ required: true }]
                                                    })(
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{ toolbar: ['undo', 'redo'] }}/>
                                                    )}
                                                </Col>
                                            </Row>
                                        </FormItem>
                                    </Row>
                                    }
                                </Panel>
                                <Panel header={<h3> Applications Rejection Automation</h3>} key="2"
                                       style={customPanelStyle}>
                                    <Form.Item label="Auto reject applicants "
                                               help="Select the percentage to auto reject the applicants">
                                        {getFieldDecorator('RejectApplications', {
                                            valuePropName: 'checked',
                                            initialValue: autoPilot?.RejectApplications
                                        })(
                                            <Switch style={{ marginRight: 15 }}/>
                                        )}
                                        A score lower than
                                        {getFieldDecorator('RejectionScore', {
                                            initialValue: (autoPilot?.RejectionScore * 100).toFixed(2),
                                            rules: [{ required: true }],
                                            hidden: !getFieldValue('RejectApplications')
                                        })(
                                            <InputNumber min={1} max={100}
                                                         style={{ marginLeft: 15 }}
                                                         formatter={value => `${value}%`}
                                                         disabled={!getFieldValue('RejectApplications')}/>
                                        )}
                                    </Form.Item>

                                    <FormItem label="Auto send rejection email"
                                              help="Rejected applicants will be notified via email if email is provided in the chat (candidates applications only)">
                                        {getFieldDecorator('SendRejectionEmail', {
                                            initialValue: autoPilot?.SendRejectionEmail,
                                            valuePropName: 'checked',
                                            rules: []
                                        })(
                                            <Switch disabled={!getFieldValue('RejectApplications')}/>
                                        )}
                                    </FormItem>

                                    {getFieldValue('SendRejectionEmail') &&
                                    <FormItem label="Rejection Email Title">
                                        {getFieldDecorator('RejectionEmailTitle', {
                                            initialValue: autoPilot?.RejectionEmailTitle,
                                            rules: [{ required: true }],
                                            hidden: !getFieldValue('RejectApplications')

                                        })(
                                            <Input placeholder="Sorry you got rejected"
                                                   disabled={!getFieldValue('RejectApplications')}/>
                                        )}
                                    </FormItem>
                                    }
                                    {getFieldValue('SendRejectionEmail') &&
                                    <Row className={styles.CEKwrapper}>
                                        <FormItem label="Rejection Email Body">
                                            <ButtonGroup style={{ margin: '5px 0' }}>
                                                <Button
                                                    onClick={() => this.appendFormKV('RejectionEmailBody', ' ${candidateName}$')}>
                                                    Candidate Name
                                                </Button>
                                                <Button
                                                    onClick={() => this.appendFormKV('RejectionEmailBody', ' ${candidateEmail}$')}>
                                                    Candidate Email
                                                </Button>
                                            </ButtonGroup>
                                            <Row>
                                                <Col span={15}>
                                                    {getFieldDecorator('RejectionEmailBody', {
                                                        initialValue: autoPilot?.RejectionEmailBody,
                                                        rules: [{ required: true }],
                                                        hidden: !getFieldValue('RejectApplications')
                                                    })(
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{ toolbar: toolbar }}
                                                            disabled={!getFieldValue('RejectApplications')}/>
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
                                            valuePropName: 'checked',
                                            rules: []
                                        })(
                                            <Switch disabled={!getFieldValue('RejectApplications')}/>
                                        )}
                                    </FormItem>

                                    {getFieldValue('SendRejectionSMS') &&
                                    <Row className={styles.CEKwrapper}>
                                        <FormItem label="Rejection SMS Body">
                                            <ButtonGroup style={{ margin: '5px 0' }}>
                                                <Button
                                                    onClick={() => this.appendFormKV('RejectionSMSBody', ' ${candidateName}$')}>
                                                    Candidate Name
                                                </Button>
                                                <Button
                                                    onClick={() => this.appendFormKV('RejectionSMSBody', ' ${candidateEmail}$')}>
                                                    Candidate Email
                                                </Button>
                                            </ButtonGroup>
                                            <Row>
                                                <Col span={15}>
                                                    {getFieldDecorator('RejectionSMSBody', {
                                                        initialValue: autoPilot?.RejectionSMSBody,
                                                        rules: [{ required: true }],
                                                        hidden: !getFieldValue('SendRejectionSMS')
                                                    })(
                                                        <CKEditor
                                                            editor={ClassicEditor}
                                                            config={{ toolbar: ['undo', 'redo'] }}/>
                                                    )}
                                                </Col>
                                            </Row>
                                        </FormItem>
                                    </Row>
                                    }
                                </Panel>
                            </Collapse>
                            <br/>
                            <h2>Appointments</h2>
                            <Collapse defaultActiveKey={openCollapse2}>
                                <Panel header={<h3> Manage Appointments Automation</h3>} key="1"
                                       style={customPanelStyle}>
                                    <FormItem label="Auto manage and send candidates appointments"
                                              help="Accepted candidates will receive an email (if provided) to pick
                                            a time slot for an appointment. You can then confirm these
                                            appointments from the Appointments page"

                                    >
                                        {getFieldDecorator('SendCandidatesAppointments', {
                                            initialValue: autoPilot.SendCandidatesAppointments,
                                            valuePropName: 'checked',
                                            rules: []
                                        })(
                                            <Switch/>
                                        )}
                                    </FormItem>
                                    <Form.Item
                                        label="Time table"
                                        help="Select a time table to be used for automatic appointment slots generation">
                                        {getFieldDecorator('AppointmentAllocationTimes', {
                                            initialValue: this.props.autoPilot?.AppointmentAllocationTimeID,
                                            rules: [{
                                                required: getFieldValue('SendCandidatesAppointments'),
                                                message: 'Select a time table'
                                            }]
                                        })(
                                            <Select
                                                disabled={!getFieldValue('SendCandidatesAppointments')}
                                                dropdownRender={menu => (
                                                    <div>
                                                        {menu}
                                                        <Divider style={{ margin: '4px 0' }}/>
                                                        <div
                                                            onMouseDown={() => history.push(`/dashboard/appointments?tab=TimeSlots`)}
                                                            style={{ padding: '8px', cursor: 'pointer' }}>
                                                            <Icon type="plus"/> Create time table
                                                        </div>
                                                    </div>
                                                )}>
                                                {this.props.appointmentAllocationTime.map((time, i) => {
                                                    return (
                                                        <Select.Option key={i}
                                                                       value={time.ID}>{time.Name}</Select.Option>);
                                                })}
                                            </Select>
                                        )}

                                    </Form.Item>
                                </Panel>
                            </Collapse>
                        </Form>
                    }


                    <Button type={'primary'} size={'large'} onClick={this.onSubmit} style={{ marginTop: 30 }}>
                        Save changes
                    </Button>

                    <Button type={'danger'} size={'large'} style={{ marginTop: 30 }} onClick={this.handleDelete}>Delete
                        Auto Pilot</Button>
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
        aatLoading: state.appointmentAllocationTime.isLoading
    };
}

export default connect(mapStateToProps)(Form.create()(AssistantAutoPilot)); 