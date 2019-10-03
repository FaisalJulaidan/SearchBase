import React from 'react';
import {Button, Input, Typography} from "antd";
import {getLink} from "helpers/links";

const {Title, Paragraph, Text} = Typography;


export const VincereFeatures = () =>
    <Typography style={{padding: '0 60px'}}>
        <Title>Introduction</Title>
        <Paragraph>
            We currently offer a full all-round integration with Vincere. You can simply login with your Vincere
            credentials and we will read and write all of data processed by our platform and the chatbots that you have
            created.
        </Paragraph>

        <Paragraph>
            For your integration to start, you will need to request some information from Vincere.
            What you’ll need:
            <ul>
                <li>Username</li>
                <li>Password</li>
            </ul>
        </Paragraph>
        <Paragraph>
            You can request both information by heading to this link:
            <Text code style={{margin: '0 0 0 5px'}}>
                <a href="https://www.Vincere.com/uk/technical-support-2/" target={'_blank'}
                   style={{cursor: 'pointer'}}>
                    https://www.Vincere.com/uk/technical-support-2/
                </a>
            </Text>.
        </Paragraph>

        <Paragraph>
            Once you have the necessary information, you can simply start using Vincere + TheSearchBase.
        </Paragraph>

        <Title level={2}>Guidelines and Resources</Title>
        <Paragraph>
            You can request more information about our Vincere CRM integration by emailing us at:
            <Text code><a target={'_blank'}
                          href={"mailto:info@thesearchbase.com"}
                          style={{cursor: 'pointer'}}>
                info@thesearchbase.com
            </a></Text>.
        </Paragraph>
    </Typography>;

export const VincereHeader = () =>
    <Paragraph type="secondary">
        Vincere description
    </Paragraph>;

export const VincereFormItems = ({
                                     FormItem,
                                     layout,
                                     getFieldDecorator,
                                     validateFields
                                 }) =>
    <>
        <FormItem label="Domain"
                  {...layout}>
            {getFieldDecorator('domain', {
                rules: [{
                    required: true,
                    message: "Please add your domain name",
                }],
            })(
                <Input placeholder={'E.g: thesearchbase(.vincere.io)'}/>
            )}
        </FormItem>


        <Button type="primary"
                icon={'login'}
                style={{width: 'auto'}}
                onClick={
                    () => validateFields((err, values) =>
                        window.location =
                            "https://id.vincere.io/oauth2/authorize?client_id=14e3d987-7f09-4aa0-af7c-9192f02d545f&response_type=code&redirect_uri=" +getLink("/dashboard/marketplace/Vincere")+"&state="+values.domain
                    )
                }
                size={'large'}>
            Connect
        </Button>

    </>;


