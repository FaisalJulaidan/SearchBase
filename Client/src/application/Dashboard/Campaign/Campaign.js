import React from 'react';
import {connect} from 'react-redux';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Typography, Form, Input, Icon, Button, Tag, AutoComplete, Select, Switch, Row, Col} from 'antd';

import {trimText} from "../../../helpers";

import googleMaps from '@google/maps'

import Phone from "../../../components/Phone/Phone";
import styles from "./Campaign.module.less";
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
            locations: [],
            skills: [],
            skillInput: "",
            textMessage:""
        };
        this.setLocations = this.setLocations.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.addCandidateName = this.addCandidateName.bind(this);
    }

    componentWillMount() {
        this.props.dispatch(campaignActions.fetchCampaignData());
    }

    findLocation = (value) => {
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
        let textMessage = this.state.textMessage+" {candidate.name} ";
        this.props.form.setFieldsValue({text: textMessage}); //Update Message Input
        this.setState({textMessage:textMessage}); //Update TextMessage State for Phone.JS
    };

    //TODO:: Skill should be validated before submission | Empty String can be accepted
    submit = (e) => {
        if (e.key === "Enter") {
            this.setState({skills: this.state.skills.concat([e.target.value])});
            this.props.form.setFieldsValue({skill: ""});
        }
    };

    handleSubmit = (event) => {
        event.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.dispatch(campaignActions.launchCampaign(
                    values.assistant_id,
                    this.state.use_crm,
                    values.crm_id,
                    values.database_id,
                    values.messenger_id,
                    values.location,
                    values.jobTitle,
                    this.state.skills,
                    this.state.textMessage,
                ));
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
            <div className={styles.mainContainer}>
                <div className={styles.formContainer}>
                    <Form layout='vertical' onSubmit={this.handleSubmit}>
                        <FormItem label={"Assistant"}>
                            {getFieldDecorator("assistant_id", {
                                rules: [{
                                    required: true,
                                    message: "Please select the assistant"
                                }],
                            })(
                                <Select placeholder={"Please select the assistant"}>
                                    {(() => {
                                        return this.props.assistants.map((item, key) => {
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
                        <FormItem label={"Use CRM"} labelCol={{xs: {span: 5, offset: 0}}}>
                            <Switch onChange={(checked) => this.setState({use_crm: checked})}
                                    defaultChecked={this.state.use_crm}/>
                        </FormItem>
                        {(() => {
                            if (this.state.use_crm) {
                                return (
                                    <FormItem label={"CRM Type"}>
                                        {getFieldDecorator("crm_id", {
                                            rules: [{
                                                required: true,
                                                message: "Please select your desired CRM"
                                            }],
                                        })(
                                            <Select placeholder={"Please select your desired CRM"}>
                                                {(() => {
                                                    return this.props.crms.map((item, key) => {
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
                                );
                            } else {
                                return (
                                    <FormItem label={"Database"}>
                                        {getFieldDecorator("database_id", {
                                            rules: [{
                                                required: true,
                                                message: "Please select the database"
                                            }],
                                        })(
                                            <Select placeholder={"Please select the database"}>
                                                {(() => {
                                                    return this.props.databases.map((item, key) => {
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
                                );
                            }
                        })()}
                        <FormItem label={"Messaging Service"}>
                            {getFieldDecorator("messenger_id", {
                                rules: [{
                                    required: true,
                                    message: "Please select the messaging service"
                                }],
                            })(
                                <Select placeholder={"Please select the messaging service"}>
                                    {(() => {
                                        return this.props.messengers.map((item, key) => {
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
                        <FormItem label={"Job Title"}>
                            {getFieldDecorator("jobTitle", {
                                rules: [{
                                    whitespace: true,
                                    required: true,
                                    message: "Please enter your job title"
                                }],
                            })(
                                <Input placeholder={"Please enter your job title"}/>
                            )}
                        </FormItem>
                        <FormItem label={"Skills"}>
                            {getFieldDecorator("skill", {
                                setFieldsValue: this.state.skillInput
                            })(
                                <Input placeholder="Type in a skill and press enter to add to the list of skills"
                                       type="text"
                                       onKeyDown={this.submit}
                                       onChange={e => this.setState({skillInput: e.target.value})}/>
                            )}
                        </FormItem>
                        <div>
                            {this.state.skills.map((skill, i) => {
                                return (<Tag closable key={i}>{skill}</Tag>)
                            })}
                        </div>
                        <FormItem label={"Location"}>
                            {getFieldDecorator("location")(
                                <AutoComplete placeholder="Type in your location"
                                              type="text"
                                              dataSource={this.state.locations}
                                              onChange={value => this.findLocation(value)}/>
                            )}
                        </FormItem>
                        <FormItem label={"Message"}>
                            <Row gutter={16} type="flex" justify="end">
                                <Col span={24}>
                                    {getFieldDecorator("text")(
                                        <TextArea placeholder="Type in the message you'd like to send"
                                                  onChange={e => this.setState({textMessage: e.target.value})}
                                        />
                                    )}
                                </Col>
                                <Col span={7}>
                                    <Button type="default" shape="round" size="small"
                                            onClick={this.addCandidateName}>
                                        Candidate Name
                                    </Button>
                                </Col>
                            </Row>
                        </FormItem>
                        <Button type="primary" icon="rocket" onClick={this.handleSubmit} size={"large"}>
                            Launch
                        </Button>
                    </Form>
                </div>
                <div className={styles.phoneContainer}>
                    <h1 className={styles.phoneTitle}>Demo</h1>
                    <Phone messages={this.state.textMessage === "" ? [] : [this.state.textMessage]}/>
                </div>
            </div>

        </NoHeaderPanel>)
    }

}

function mapStateToProps(state) {
    return {
        assistants: state.campaign.assistants,
        crms: state.campaign.crms,
        databases: state.campaign.databases,
        messengers: state.campaign.messengers,
        isLoading: state.campaign.isLoading,
        isLaunching: state.campaign.isLaunching
    };
}

export default connect(mapStateToProps)(Form.create()(Campaign));
