import React from 'react';
import {connect} from 'react-redux';
import moment from 'moment';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Typography, Form, Input, Icon, Button, Tag, AutoComplete} from 'antd';

import googleMaps from '@google/maps'

import Phone from "../../../components/Phone/Phone";
import styles from "./Campaign.module.less";

const FormItem = Form.Item;

const {Title, Paragraph} = Typography;
const { TextArea } = Input;

const google = googleMaps.createClient({
    key: 'AIzaSyDExVDw_47y0U4kukU1A0UscjXE7qDTRhk'
});

let skills = ["Software engineer", "Sales"];

class Campaign extends React.Component {
    constructor(props) {
        super(props)
        this.timer = React.createRef()
        this.state = {
            skills: [],
            skillInput: "",
            location: "",
            locations: [],
            textMessage: ""
        }
        this.setLocations = this.setLocations.bind(this)
    }

    findLocation = (value) => {
        clearTimeout(this.timer.current)
        this.timer.current = setTimeout(() => {
            google.geocode({
                address: value
            }, this.setLocations);
        }, 300)
    }

    setLocations = (err, response) => {
        if (!err) {
            let resp = response.json.results.filter(address => address.address_components.find(loc => loc.types.includes("country")).short_name === "GB")
            this.setState({locations: resp.map(item => item.formatted_address)})
        }
    }

    submit = (e) => {
        if(e.key === "Enter"){
            this.setState({skills: this.state.skills.concat([e.target.value]), skillInput: ""})
        }
    }


    render() {
        const { form } = this.props;
        const { getFieldDecorator } = form;

        return (<NoHeaderPanel>
            <div className={styles.Header}>
                <Title className={styles.Title}>
                    <Icon type="rocket"/> Campaign Outreach
                </Title>
                <Paragraph type="secondary">
                    Here you can use our Outreach engine to Engage with the candidates inside your CRM via SMS and Email. Campaigns are a great way for you to keep your CRM or database refreshed with GDPR compliant information.
                </Paragraph>
            </div>
            <div className={styles.mainContainer}>
                <div className={styles.formContainer}>
                    <Form layout='vertical' onSubmit={this.handleSubmit}>
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
                        <FormItem
                            label={"Skills"}
                            >
                            <Input placeholder="Type in a skill and press enter to add to the list of skills"
                                   type="text"
                                   onKeyDown={this.submit}
                                   onChange={e => this.setState({skillInput: e.target.value})} value={this.state.skillInput}/>

                        </FormItem>
                        <div>
                        {this.state.skills.map((skill, i) => {
                            return (<Tag closable key={i}>{skill}</Tag>)
                        })}
                        </div>
                        <FormItem label={"Location"}>
                            <AutoComplete placeholder="Type in your location"
                                         type="text"
                                          dataSource={this.state.locations}
                                onChange={value => this.findLocation(value)}/>

                        </FormItem>
                        <FormItem label={"Message"}>
                            <TextArea placeholder="Type in the message you'd like to send"
                                    onChange={e => this.setState({textMessage: e.target.value})}/>

                        </FormItem>
                        <Button type="primary" icon="rocket" size={"large"}>
                            Launch
                        </Button>
                    </Form>
                </div>
                <div className={styles.phoneContainer}>
                    <h1 className={styles.phoneTitle}>Demo</h1>
                    <Phone messages={this.state.textMessage === "" ? [] : [this.state.textMessage]} />
                </div>
            </div>

        </NoHeaderPanel>)
    }

}


export default Form.create()(Campaign)
