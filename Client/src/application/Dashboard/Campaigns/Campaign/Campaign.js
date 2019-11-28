import React from 'react';
import {connect} from 'react-redux';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {
    Typography, Form, Input, Icon, Divider, Button, Tag, AutoComplete, Select, Switch, Modal,
    List, Checkbox, Spin, Radio, Slider, InputNumber
} from 'antd';

import {trimText} from "../../../../helpers";

import googleMaps from '@google/maps'

import Phone from "../../../../components/Phone/Phone";
import styles from "./Campaign.module.less";
import {history} from 'helpers';
import {campaignActions} from "store/actions";

const FormItem = Form.Item;

const {Title, Paragraph} = Typography;
const {TextArea} = Input;

const google = googleMaps.createClient({
    key: 'AIzaSyDExVDw_47y0U4kukU1A0UscjXE7qDTRhk'
});

class Campaign extends React.Component {


    constructor(props) {
        super(props);
        this.timer = React.createRef();
        this.state = {
            use_crm: true,
            location: "",
            locations: [],
            distance: 50,
            skills: [],
            candidate_list: [],
            candidatesModalVisibility: false,
            campaignNameModalVisibility: false,
            skillInput: "",
            textMessage: "",
            isSaved: true, //check if the campaign is saved or not
            campaignName: "",
            outreach_type: "sms",
            assistantLinkInMessage: false,
            selectedCRM: null,
            useShortlist: false
        };
    }

    componentDidMount() {
        let id = this.props.match.params.id;
        if (id === 'new') {
            this.props.dispatch(campaignActions.fetchCampaigns());
            this.setState({isSaved: false})
        } else {
            this.props.dispatch(campaignActions.fetchCampaign(id))
                .then(() => {
                    let campaign = this.props.campaign;
                    this.setState({
                        skills: JSON.parse(campaign?.Skills.replace(/'/g, '"')), //Fix JSON with REGEXP
                        textMessage: campaign?.Message,
                        use_crm: campaign?.UseCRM,
                        location: campaign?.Location,
                        assistantLinkInMessage: campaign?.Message.indexOf("{assistant.link}") !== -1,
                        selectedCRM: campaign?.CRMID,
                        useShortlist: campaign?.useShortlist
                    }, state => console.log(this.state));
                    this.props.form.setFieldsValue({
                        name: trimText.capitalize(trimText.trimDash(campaign?.Name)),
                        assistant_id: campaign?.AssistantID,
                        crm_id: campaign?.CRMID,
                        shortlist_id: campaign?.shortlistID,
                        database_id: campaign?.DatabaseID,
                        messenger_id: campaign?.MessengerID,
                        location: campaign?.Location,
                        jobTitle: campaign?.JobTitle,
                        text: campaign?.Message,
                    });
                }).catch((err) => {
                console.log(err);
                history.push(`/dashboard/campaigns`)
            });
        }
        if (this.state.textMessage.indexOf("{assistant.link}") !== -1 && this.state.assistantLinkInMessage) {
            this.setState({assistantLinkInMessage: true})
        }
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.isCandidatesLoading && (this.props.errorMsg === null)) {
            this.state.candidate_list = this.props.candidate_list;
            this.showModal(true);
        } else if (prevProps.isLaunchingCampaign && (this.props.errorMsg === null)) {
            this.showModal(false);
        }

        let linkInMessage = this.state.textMessage.indexOf("{assistant.link}") !== -1

        if (linkInMessage !== this.state.assistantLinkInMessage) {
            this.setState({assistantLinkInMessage: linkInMessage})
        }
    };

    componentWillUnmount() {
        clearTimeout(this.timer.current)
    }

    showModal = (visibility) => {
        if (this.state.candidatesModalVisibility !== visibility)
            this.setState({candidatesModalVisibility: visibility,});
    };

    findLocation = (value) => {
        this.setState({location: value});
        clearTimeout(this.timer.current);
        this.timer.current = setTimeout(() => {
            google.geocode({
                address: value
            }, this.setLocations);
        }, 300)
    };

    setLocations = (err, response) => {
        if (!err) {
            // GB Filter (in the future to remove replace with let resp = response.json.results.filter(address => address.address_components)
            let resp = response.json.results.filter(address => address.address_components.find(loc => loc.types.includes("country")).short_name === "GB");
            this.setState({locations: resp.map(item => item.formatted_address)})
        }
    };

    addCandidateName = () => {
        let textMessage = this.state.textMessage + " {candidate.name} ";
        this.props.form.setFieldsValue({text: textMessage}); //Update Message Input
        this.setState({textMessage: textMessage}); //Update TextMessage State for Phone.JS
    };

    addAssistantLink = () => {
        let textMessage = this.state.textMessage + " {assistant.link} ";
        this.props.form.setFieldsValue({text: textMessage}); //Update Message Input
        this.setState({textMessage: textMessage}); //Update TextMessage State for Phone.JS
    };

    //TODO:: Skill should be validated before submission | Empty String can be accepted
    handleSkillSubmit = (e) => {
        if (e.target.value.length === 0)
            return;
        this.setState({skills: this.state.skills.concat([e.target.value])});
        this.props.form.setFieldsValue({skill: ""});
    };

    onSkillTagClose = (value) => {
        let skills = this.state.skills.filter(function (skill) {
            if (skill !== value)
                return skill
        });
        this.setState({skills: skills});
    };

    handleModalLaunch = () => {

        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.launchCampaign(values)
            }
        });
    };

    launchCampaign = (values) => {
        this.props.dispatch(campaignActions.launchCampaign(
            values.assistant_id,
            this.state.use_crm,
            values.crm_id,
            this.state.useShortlist,
            values.shortlist_id,
            values.database_id,
            values.messenger_id,
            values.location,
            values.jobTitle,
            values.jobType,
            this.state.skills,
            values.text,
            this.state.candidate_list,
            values.outreach_type,
            values.email_title
        ));
    };

    handleModalSelectAll = () => {
        if (this.props?.candidate_list?.length === this.state.candidate_list.length)
            this.setState({candidate_list: []});
        else
            this.setState({candidate_list: this.props.candidate_list})
    };

    handleModalCancel = () => {
        this.setState({candidatesModalVisibility: false, campaignNameModalVisibility: false});
    };

    afterModalClose = () => {
        this.setState({candidate_list: []});
    };

    onCandidateSelected = (e, candidate) => {
        if (e.target.checked)
            this.state.candidate_list.push(candidate);
        else {
            this.state.candidate_list = this.state.candidate_list.filter(function (tempCandidate) {
                if (tempCandidate.ID !== candidate.ID)
                    return tempCandidate
            });
        }
        this.setState({candidate_list: this.state.candidate_list});
    };

    isCandidateSelected = (candidate) => {
        return this.state.candidate_list.some((tempCandidate) => {
            if (tempCandidate.ID === candidate.ID)
                return true;
        });
    };

    handleLaunch = (event) => { //Handle Launch
        event.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                if (!this.state.assistantLinkInMessage) {
                    Modal.confirm({
                        title: 'You have not put the Assistant\'s Link in your message!',
                        content: `Do you wish to proceed?`,
                        okText: 'Yes',
                        okType: 'ghost',
                        cancelText: 'No',
                        onOk: () => this.searchCandidates(values)
                    });
                } else {
                    this.searchCandidates(values)
                }
            }
        });
    };

    searchCandidates = (values) => {
        this.props.dispatch(campaignActions.fetchCampaignCandidatesData(
            values.assistant_id,
            this.state.use_crm,
            values.crm_id,
            this.state.useShortlist,
            values.shortlist_id,
            values.database_id,
            values.messenger_id,
            values.location,
            values.jobTitle,
            values.jobType,
            this.state.skills,
            this.state.textMessage,
            values.outreach_type,
            values.email_title,
        ));
    };


    handleSave = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                if (this.state.isSaved) {
                    this.props.dispatch(campaignActions.updateCampaign(
                        this.props.campaign.ID,
                        values.name,
                        values.assistant_id,
                        this.state.use_crm,
                        values.crm_id,
                        this.state.useShortlist,
                        values.shortlist_id,
                        values.database_id,
                        values.messenger_id,
                        values.location,
                        values.jobTitle,
                        this.state.skills,
                        this.state.textMessage,
                    ));
                } else {
                    this.setState({campaignNameModalVisibility: true})
                }
            }
        });
    };

    handleSaveNewCampaign = () => {
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.dispatch(campaignActions.saveCampaign(
                    this.state.campaignName,
                    values.assistant_id,
                    this.state.use_crm,
                    values.crm_id,
                    this.state.useShortlist,
                    values.shortlist_id,
                    values.database_id,
                    values.messenger_id,
                    values.location,
                    values.jobTitle,
                    this.state.skills,
                    this.state.textMessage,
                )).then(() => {
                    this.setState({campaignNameModalVisibility: false});
                    history.push('/dashboard/campaigns')
                });
            }
        });
    };

    handleDelete = () => {
        Modal.confirm({
            title: 'Are you sure delete this campaign?',
            content: `If you click YES, this campaign data will be deleted.`,
            okText: 'Yes',
            okType: 'danger',
            cancelText: 'No',
            onOk: () => {
                this.props.dispatch(campaignActions.deleteCampaign(this.props.campaign.ID))
                    .then(() => history.push('/dashboard/campaigns'));
            }
        });
    };

    render() {
        const {form} = this.props;
        const {getFieldDecorator} = form;
        return (<NoHeaderPanel>
            <div className={styles.Header}>
                <Title className={styles.Title}>
                    <Icon type="rocket"/> Campaign Outreach
                </Title>
                <Paragraph type="secondary">
                    Here you can use our Outreach engine to Engage with the candidates inside your CRM via SMS and
                    Email. Campaigns are a great way for you to keep your CRM or database refreshed with GDPR compliant
                    information.
                </Paragraph>
            </div>
            {this.state.isSaved && this.props.isLoading ? <Spin/> :
                <div className={styles.mainContainer}>

                    <Modal
                        title="Please select candidates"
                        centered
                        visible={this.state.candidatesModalVisibility}
                        okText={"Launch"}
                        onOk={this.handleModalLaunch}
                        confirmLoading={this.props.isLaunchingCampaign}
                        okButtonProps={{icon: "rocket"}}
                        footer={<div>
                            <Button onClick={this.handleModalCancel}>Cancel</Button>
                            <Button onClick={this.handleModalSelectAll}
                                    disabled={this.props?.candidate_list?.length === 0}>
                                {this.props?.candidate_list?.length === this.state.candidate_list.length ? 'Deselect all' : 'Select All'}
                            </Button>
                            <Button onClick={this.handleModalLaunch}
                                    type="primary"
                                    loading={this.props.isLaunchingCampaign}
                                    icon="rocket">Launch</Button>
                        </div>}
                        onCancel={this.handleModalCancel}
                        afterClose={this.afterModalClose}
                        destroyOnClose
                        bodyStyle={{overflow: 'auto', maxHeight: '50vh'}}
                        maskClosable={false}>
                        <List
                            loading={this.props.isCandidatesLoading}
                            itemLayout="horizontal"
                            dataSource={this.props.candidate_list}
                            renderItem={(item) => (
                                <List.Item actions={[<Checkbox defaultChecked checked={this.isCandidateSelected(item)}
                                                               onChange={(e) => this.onCandidateSelected(e, item)}/>]}>
                                    <List.Item.Meta
                                        title={<span style={{
                                            color: '#444444',
                                            fontWeight: 'bold',
                                            fontSize: '1.2em'
                                        }}>{item.CandidateName}</span>}
                                        description={<span
                                            style={{fontSize: '1.1em'}}>{item.CandidateCity + ' - ' + item.CandidateSkills}</span>}/>
                                </List.Item>
                            )}
                        />
                    </Modal>

                    <Modal
                        title="Campaign Name"
                        visible={this.state.campaignNameModalVisibility}
                        okText={"Save"}
                        onOk={this.handleSaveNewCampaign}
                        confirmLoading={this.props.isSaving}
                        onCancel={this.handleModalCancel}>
                        <Input value={this.state.campaignName} placeholder={"Please enter a name for your campaign"}
                               onChange={e => {
                                   this.setState({campaignName: e.target.value})
                               }}/>
                    </Modal>

                    <div className={styles.formContainer}>
                        <Form layout='vertical' onSubmit={this.handleLaunch}>
                            <FormItem style={{display: this.state.isSaved ? 'block' : 'none'}} label={"Campaign Name"}>
                                {getFieldDecorator("name")(
                                    <Input placeholder={"Please enter a name for your campaign"}/>
                                )}
                            </FormItem>
                            <FormItem label={"Assistant"}>
                                {getFieldDecorator("assistant_id", {
                                    rules: [{
                                        required: true,
                                        message: "Please select the assistant"
                                    }],
                                })(
                                    <Select placeholder={"Please select the assistant"} loading={this.props.isLoading}>
                                        {(() => {
                                            return this.props.campaignOptions?.assistants.map((item, key) => {
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
                            <FormItem label={"Use CRM"} labelCol={{xs: {span: 4, offset: 0}}}>
                                <Switch checked={this.state.use_crm}
                                        onChange={(checked) => this.setState({use_crm: checked})}
                                        defaultChecked={this.state.use_crm}/>
                            </FormItem>
                            {this.state.use_crm ?
                                <>
                                    <FormItem label={"CRM Type"}>
                                        {getFieldDecorator("crm_id", {
                                            ...(this.state.selectedCRM !== null && {initialValue: this.state.selectedCRM}),
                                            rules: [{
                                                required: true,
                                                message: "Please select your desired CRM"
                                            }],
                                        })(
                                            <Select placeholder={"Please select your desired CRM"}
                                                    loading={this.props.isLoading}
                                                    onSelect={value => {
                                                        this.setState({selectedCRM: value});

                                                    }}>
                                                {this.props.campaignOptions?.crms.map((item, key) => {
                                                    return (
                                                        <Select.Option key={key} value={item.ID}>
                                                            {trimText.capitalize(trimText.trimDash(item.Type))}
                                                        </Select.Option>
                                                    );
                                                })}
                                            </Select>
                                        )}
                                        {getFieldDecorator("useShortlist")(
                                            <Checkbox
                                                checked={this.state.useShortlist}
                                                onChange={(e) => {
                                                    if (e.target.checked)
                                                        this.props.dispatch(campaignActions.fetchShortlists(this.state.selectedCRM));
                                                    else {
                                                        this.props.form.setFieldsValue({shortlist_id: ""});
                                                    }
                                                    this.setState({useShortlist: e.target.checked})
                                                }}
                                                style={{
                                                    display: (
                                                        this.state.selectedCRM ===
                                                        this.props.campaignOptions?.crms.find(crm => crm.Type === 'Jobscience')?.ID
                                                            ? 'block'
                                                            : 'none'
                                                    ),
                                                    marginTop: '10px'
                                                }}>Use Jobscience Shortlist</Checkbox>
                                        )}
                                    </FormItem>
                                    <FormItem label="Shortlist" style={{
                                        display: (
                                            this.state.selectedCRM ===
                                            this.props.campaignOptions?.crms.find(crm => crm.Type === 'Jobscience')?.ID &&
                                            this.state.useShortlist ? 'block' : 'none')
                                    }}
                                    >
                                        {getFieldDecorator("shortlist_id", {
                                            rules: [{
                                                required: this.state.useShortlist,
                                                message: "Please select a shortlist"
                                            }],
                                        })(
                                            <Select placeholder={"Please select a shortlist"}
                                                    loading={this.props.isLoadingShortlists}>
                                                {this.props.shortlists?.map((item, key) => {
                                                    return (
                                                        <Select.Option key={key} value={item.url}>
                                                            {trimText.capitalize(trimText.trimDash(item.name))}
                                                        </Select.Option>
                                                    );
                                                })}
                                            </Select>
                                        )}
                                    </FormItem>
                                </>
                                :
                                <FormItem label={"Database"}>
                                    {getFieldDecorator("database_id", {
                                        rules: [{
                                            required: true,
                                            message: "Please select the database"
                                        }],
                                    })(
                                        <Select placeholder={"Please select the database"}
                                                loading={this.props.isLoading}>
                                            {(() => {
                                                return this.props.campaignOptions?.databases.map((item, key) => {
                                                    if (item.Type?.name !== "Candidates")
                                                        return;
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
                            }


                            <FormItem label={"Outreach Type "}>
                                {getFieldDecorator("outreach_type", {initialValue: "sms"})(
                                    <Radio.Group onChange={(e) => {
                                        this.setState({outreach_type: e.target.value})
                                    }}>
                                        <Radio.Button value="sms">SMS</Radio.Button>
                                        <Radio.Button value="email">Email</Radio.Button>
                                    </Radio.Group>
                                )}
                            </FormItem>

                            <FormItem label={"Messaging Service"}
                                      style={this.state.outreach_type !== 'sms' ? {display: 'none'} : {display: 'block'}}>
                                {getFieldDecorator("messenger_id", {
                                    rules: [{
                                        required: this.state.outreach_type === 'sms',
                                        message: "Please select the messaging service"
                                    }],
                                })(
                                    <Select placeholder={"Please select the messaging service"}
                                            loading={this.props.isLoading}>
                                        {(() => {
                                            return this.props.campaignOptions?.messengers.map((item, key) => {
                                                return (
                                                    <Select.Option key={key} value={item.ID}>
                                                        {trimText.capitalize(trimText.trimDash(item.Type))}
                                                    </Select.Option>
                                                );
                                            });
                                        })()}
                                    </Select>
                                )}
                            </FormItem>
                            {this.state.useShortlist && this.state.use_crm
                            && this.state.selectedCRM ===
                            this.props.campaignOptions?.crms.find(crm => crm.Type === 'Jobscience')?.ID
                                ?
                                <>
                                </>
                                :
                                <>
                                    <FormItem label={"Job Title"}>
                                        {getFieldDecorator("jobTitle", {
                                            rules: [{
                                                whitespace: true,
                                                message: "Please enter your job title"
                                            }],
                                        })(
                                            <Input placeholder={"Please enter your job title"}/>
                                        )}
                                    </FormItem>
                                    <FormItem label={"Job Type"}>
                                        {getFieldDecorator("jobType", {initialValue: "permanent"})(
                                            <Radio.Group>
                                                <Radio.Button value="permanent">Permanent</Radio.Button>
                                                <Radio.Button value="temporary">Temporary</Radio.Button>
                                                <Radio.Button value="contract">Contract</Radio.Button>
                                            </Radio.Group>
                                        )}
                                    </FormItem>
                                    <FormItem label={"Skills"}>
                                        {getFieldDecorator("skill")(
                                            <Input
                                                placeholder="Type in a skill and press enter to add to the list of skills"
                                                type="text"
                                                onPressEnter={this.handleSkillSubmit}/>
                                        )}
                                    </FormItem>
                                    <div>
                                        {this.state.skills.map((skill, i) => {
                                            return (<Tag visible closable key={i} onClose={() => {
                                                this.onSkillTagClose(skill)
                                            }}>{skill}</Tag>)
                                        })}
                                    </div>
                                    <FormItem label={"Location"}>
                                        {getFieldDecorator("location", {
                                            rules: [{
                                                whitespace: true,
                                                message: "Please enter the location"
                                            }],
                                            initialValue: this.state.location
                                        })(
                                            <AutoComplete placeholder="Type in your location"
                                                          type="text"
                                                          dataSource={this.state.locations}
                                                          onChange={value => this.findLocation(value)}/>
                                        )}
                                    </FormItem>
                                    <FormItem label={`Distance within ${this.state.distance} miles`}
                                              style={{display: this.state.location ? 'block' : 'none'}}>
                                        {getFieldDecorator("distance", {initialValue: this.state.distance})(
                                            <Slider
                                                step={5}
                                                onChange={(value) => {
                                                    this.setState({distance: value})
                                                }}
                                            />
                                        )}
                                    </FormItem>
                                </>
                            }

                            <FormItem label={"Email Title "}
                                      style={this.state.outreach_type !== 'email' ? {display: 'none'} : {display: 'block'}}>
                                {getFieldDecorator("email_title", {
                                    rules: [{
                                        whitespace: true,
                                        required: this.state.outreach_type === 'email',
                                        message: "Please enter a title for your outreach email"
                                    }],
                                })(
                                    <Input placeholder="Please enter a title for your outreach email"
                                           type="text"
                                           onPressEnter={this.handleSkillSubmit}/>
                                )}
                            </FormItem>

                            <FormItem
                                label={<span>Message
                                <Button type="default" size="small" shape="round"
                                        style={{margin: '0 5px', fontSize: '.9em', borderColor: 'red'}}
                                        onClick={this.addAssistantLink}>Assistant Link</Button>
                                <Button type="default" size="small" shape="round"
                                        style={{margin: '0 5px', fontSize: '.9em'}}
                                        onClick={this.addCandidateName}>Candidate Name</Button>
                            </span>}>
                                {getFieldDecorator("text", {
                                    rules: [{
                                        required: true,
                                        message: "Please enter the message"
                                    }],
                                })(
                                    <TextArea placeholder="Type in the message you'd like to send"
                                              onChange={e => this.setState({textMessage: e.target.value})}
                                    />
                                )}
                            </FormItem>

                            <FormItem label={"Follow up every:"}>
                                {getFieldDecorator("followUp", {initialValue: "never"})(
                                    <Radio.Group onChange={(e) => {
                                        this.setState({followUp: e.target.value})
                                    }}>
                                        <Radio.Button value="never">Never</Radio.Button>
                                        <Radio.Button value="6">6 hours</Radio.Button>
                                        <Radio.Button value="12">12 hours</Radio.Button>
                                        <Radio.Button value="24">1 day</Radio.Button>
                                        <Radio.Button value="71">3 days</Radio.Button>
                                    </Radio.Group>
                                )}
                            </FormItem>

                            <FormItem label={"Schedule for every:"}>
                                {getFieldDecorator("schedule", {initialValue: "never"})(
                                    <Radio.Group onChange={(e) => {
                                        this.setState({schedule: e.target.value})
                                    }}>
                                        <Radio.Button value="never">Never</Radio.Button>
                                        <Radio.Button value="1">1 Day</Radio.Button>
                                        <Radio.Button value="7">7 Days</Radio.Button>
                                        <Radio.Button value="30">1 Month</Radio.Button>
                                        <Radio.Button value="90">3 Months</Radio.Button>
                                        <Radio.Button value="custom">Custom</Radio.Button>
                                    </Radio.Group>
                                )}
                                {this.state.schedule === 'custom' ?
                                    <InputNumber placeholder="Custom schedule, in days"
                                                 min={1}
                                                 style={{marginTop: 10, width: '30%'}}
                                                 value={this.state.customSchedule ? this.state.customSchedule : 3}
                                                 formatter={value => value == '1' ? `${value} day` : `${value} days`}
                                                 parser={value => {
                                                     value.replace('day', 'days');
                                                     value.replace('days', '');
                                                 }}
                                                 onChange={(value) => {
                                                     this.setState({customSchedule: value});
                                                 }}/>
                                    : null}
                            </FormItem>


                            <Button loading={this.props.isCandidatesLoading} icon="rocket" type="primary"
                                    onClick={this.handleLaunch}
                                    size={"large"}>
                                Launch
                            </Button>

                            <Divider/>

                            <Button loading={this.props.isDeleting} type="danger" icon="delete"
                                    onClick={this.handleDelete}
                                    style={{display: this.state.isSaved ? 'unset' : 'none'}}>
                                Delete Campaign
                            </Button>
                            <Button loading={this.props.isSaving} type="primary" icon="save" onClick={this.handleSave}>
                                {this.state.isSaved ? 'Update Campaign' : 'Save Campaign'}
                            </Button>
                        </Form>
                    </div>
                    <div className={styles.phoneContainer}>
                        <h1 className={styles.phoneTitle}>Demo</h1>
                        <Phone messages={this.state.textMessage === "" ? [] : [this.state.textMessage]}/>
                    </div>
                </div>}

        </NoHeaderPanel>)
    }

}

function mapStateToProps(state) {
    return {
        campaign: state.campaign.campaign,
        campaignOptions: state.campaign.campaignOptions,
        candidate_list: state.campaign.candidate_list,
        isLoading: state.campaign.isLoading,
        isCandidatesLoading: state.campaign.isCandidatesLoading,
        isLaunchingCampaign: state.campaign.isLaunchingCampaign,

        isLoadingShortlists: state.campaign.isLoadingShortlists,
        shortlists: state.campaign.shortlists,

        isSaving: state.campaign.isSaving,
        isDeleting: state.campaign.isDeleting,
        errorMsg: state.campaign.errorMsg
    };
}

export default connect(mapStateToProps)(Form.create()(Campaign));
