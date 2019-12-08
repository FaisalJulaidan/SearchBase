import React from 'react';
import {Button, Icon, Input, Select, Typography} from "antd";
import {getLink} from "helpers";

const {Option} = Select;
const {Title, Paragraph, Text} = Typography;

export const TwilioFormItems = ({
                                   FormItem,
                                   layout,
                                   getFieldDecorator,
                                   marketplace,
                                   connectMarketplace,
                                   isConnecting,
                                   isTesting,
                               }) =>
    <>
        {
            marketplace.status !== "CONNECTED" &&
            marketplace.status !== "FAILED" &&
            <div>
                <FormItem label="Account SID"
                          {...layout}>
                    {getFieldDecorator('account_sid', {
                        rules: [{
                            required: true,
                            message: "Please add your Account SID",
                        }],
                    })(
                        <Input placeholder={'Starting AC...'}/>
                    )}
                </FormItem>

                <FormItem label="Messaging Service SID"
                          {...layout}>
                    {getFieldDecorator('messaging_service_sid', {
                        rules: [{
                            required: true,
                            message: "Please add your Messaging Service SID",
                        }],
                    })(
                        <Input placeholder={'Starting M...'}/>
                    )}
                </FormItem>

                <FormItem label="Auth Token"
                          {...layout}>
                    {getFieldDecorator('auth_token', {
                        rules: [{
                            required: true,
                            message: "Auth Token is required",
                        }],
                    })(
                        <Input placeholder={'Your Auth Token'}/>
                    )}
                </FormItem>

                {
                    marketplace.status === "NOT_CONNECTED" &&
                    <Button type="primary" disabled={isConnecting || isTesting}
                            onClick={connectMarketplace}>Connect</Button>
                }
            </div>
        }

        {
            marketplace.status === "CONNECTED" &&
            <div style={{textAlign: 'center'}}>
                <img src={getLink('/static/images/undraw/success.svg')} alt="" height={300}/>
                <Typography.Title>
                    {marketplace.type} is connected
                </Typography.Title>
            </div>
        }

        {
            marketplace.status === "FAILED" &&
            <div style={{textAlign: 'center'}}>
                <img src={getLink('/static/images/undraw/failed.svg')} alt="" height={300}/>
                <Title>
                    {marketplace.type} is failed
                </Title>
                <Paragraph type="secondary">
                    {marketplace.type} is failing this is usually not from us, please contact the marketplace
                    provider
                </Paragraph>
            </div>
        }
    </>;

export const TwilioFeatures = ({}) =>
    <Typography style={{padding: '0 60px'}}>
        <Title>Introduction</Title>
        {/*<Paragraph>*/}
            {/*Twilio users can very simply benefit from using their systems directly by logging in*/}
            {/*through our software to connect their CRM to our platform.*/}
        {/*</Paragraph>*/}
        {/*<Paragraph>*/}
            {/*Once you have the required information and have successfully logged in – you are all*/}
            {/*done.*/}
        {/*</Paragraph>*/}
        <Paragraph>
            What you’ll need:
            <ul>
                <li>Account SID</li>
                <li>Auth Token</li>
                <li>Specified Number</li>
            </ul>
        </Paragraph>
    </Typography>;

export const TwilioHeader = () =>
    <Paragraph type="secondary">
        Twilio two-way SMS and MMS messages allow you to carry on a conversation by both sending and receiving text and
        multimedia messages. You can integrate all of your Chatbots to natively reach your Talent Pools, Clients and
        candidates from within SearchBase.
    </Paragraph>;
