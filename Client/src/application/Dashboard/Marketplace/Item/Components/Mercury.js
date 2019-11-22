import React from 'react';
import {Button, Input, Typography} from "antd";
import {getLink} from "helpers/links";

const {Title, Paragraph, Text} = Typography;

export const MercuryFeatures = () =>
    <Typography style={{padding: '0 60px'}}>
        <Title>Introduction</Title>
        <Paragraph>
            We currently offer a full all-round integration with Mercury. You can simply login with your Mercury
            credentials and we will read and write all of data processed by our platform and the chatbots that you have
            created.
        </Paragraph>

        <Paragraph>
            For your integration to start, you will need to request some information from Mercury.
            What you’ll need:
            <ul>
                <li>Username</li>
                <li>Password</li>
            </ul>
        </Paragraph>

        <Paragraph>
            You can request that information by contacting your account manager at Mercury.
        </Paragraph>

        <Paragraph>
            Once you have the necessary information, you can start using Mercury + TheSearchBase.
        </Paragraph>

        <Paragraph>
            If at any point you wish to log out from our system you can visit <a href="https://myapps.microsoft.com" target={'_blank'}
                style={{cursor: 'pointer'}}>
                https://myapps.microsoft.com
                </a>,
             click on the Profile Icon on the top right, go to 'Profile' and then press 'Sign out everywhere'. This will
             also disable Mercury's automatic log in.
        </Paragraph>

        <Title level={2}>Guidelines and Resources</Title>
        <Paragraph>
            You can request more information about our Mercury CRM integration by emailing us at:
            <Text code><a target={'_blank'}
                          href={"mailto:info@thesearchbase.com"}
                          style={{cursor: 'pointer'}}>
                info@thesearchbase.com
            </a></Text>.
        </Paragraph>
    </Typography>;

export const MercuryHeader = () =>
    <Paragraph type="secondary">
        Mercury xRM empowers the world’s recruiters to shortcut the recruitment process and deliver an exceptional
        client and candidate experience. Powered by Microsoft Dynamics 365, Mercury xRM is designed to fit with the way
        your people work now. Whether you choose to use Mercury xRM within a web browser, as an app, or inside Microsoft
        Outlook, you get an intuitive user interface that’s designed to work with Microsoft tools you know.
    </Paragraph>;

export const MercuryFormItems = ({
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
                <Input placeholder={'E.g: thesearchbase.crm3'}/>
            )}
        </FormItem>


        <Button type="primary"
                icon={'login'}
                style={{width: 'auto'}}
                onClick={
                    () => validateFields((err, values) =>
                        window.location =
                            `https://login.microsoftonline.com/common/oauth2/authorize?response_type=code&client_id=b49f9e03-5586-4248-8585-8640c4b2539c&response_mode=query&scope=https://admin.services.crm.dynamics.com/user_impersonation offline_access&redirect_uri=${getLink("/dashboard/marketplace/Mercury")}&state=${values.domain}`
                    )
                }
                size={'large'}>
            Connect
        </Button>

    </>;


