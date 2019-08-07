import React from 'react';
import {connect} from 'react-redux';
import moment from 'moment';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Typography, Form, Input, Icon, Button} from 'antd';
import styles from "../Calendar/Calendar.module.less";

const FormItem = Form.Item;

const {Title, Paragraph} = Typography;
const { TextArea } = Input;

class Campaign extends React.Component {

    handleSubmit = () => {
        console.log('sbumit')
    }

    render() {
        const { form} = this.props;
        const {getFieldDecorator} = form;

        return (<NoHeaderPanel>
            <div className={styles.Header}>
                <Title className={styles.Title}>
                    <Icon type="rocket"/> Campaign Outreach
                </Title>
                <Paragraph type="secondary">
                    Here you can use our Outreach engine to Engage with the candidates inside your CRM via SMS and Email. Campaigns are a great way for you to keep your CRM or database refreshed with GDPR compliant information.
                </Paragraph>
            </div>
            <div>
                <Form layout='vertical' wrapperCol={{span: 10}} onSubmit={this.handleSubmit}>
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
                    <FormItem label={"Location"}>
                        {getFieldDecorator("location", {
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: "Please enter your location"
                            }],
                        })(
                            <Input placeholder={"Please enter your location"}/>
                        )}
                    </FormItem>
                    <FormItem label={"Skills"}>
                        {getFieldDecorator("skills", {
                            rules: [{
                                whitespace: true,
                                required: true,
                                message: "Please enter your skills"
                            }],
                        })(
                            <Input placeholder={"Please enter your skills"}/>
                        )}
                    </FormItem>
                    <Button type="primary" icon="rocket" size={"large"}>
                        Launch
                    </Button>
                </Form>
            </div>
        </NoHeaderPanel>)
    }

}


export default Form.create()(Campaign)
