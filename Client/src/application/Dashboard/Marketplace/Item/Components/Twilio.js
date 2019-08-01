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
                        <Input placeholder={'Your Domain'}/>
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

                <FormItem label="Specified Phone Number"
                          {...layout}>
                    {getFieldDecorator('phone_number', {
                        rules: [{
                            required: true,
                            message: "The Phone number you got in Twilio is required",
                        }],
                    })(
                        <Input placeholder={'Bought Phone Number'}/>
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
        <Paragraph>
            Twilio users can very simply benefit from using their systems directly by logging in
            through our software to connect their CRM to our platform.
        </Paragraph>
        <Paragraph>
            Once you have the required information and have successfully logged in – you are all
            done.
        </Paragraph>
        <Paragraph>
            What you’ll need:
            <ul>
                <li>Account SID</li>
                <li>Auth Token</li>
                <li>Specified Number</li>
            </ul>
        </Paragraph>
        <Paragraph>
            We can start using your data to connect to the chatbots and help you with the
            automation of your tasks.
        </Paragraph>
        <Title level={2}>Guidelines and Resources</Title>
        <Paragraph>
            From the list below, choose your CRM or ATS for your account to be directly
            connected.
            If you need help with the setup or wish to contact us to arrange an integration with
            your
            provider,
            please contact us at:
            <Text code><a target={'_blank'}
                          href={"mailto:info@thesearchbase.com"}>
                info@thesearchbase.com
            </a></Text>.
        </Paragraph>
    </Typography>;

export const TwilioHeader = () =>
    <Paragraph type="secondary">
        Bond Twilio, specialist portfolio of recruitment software applications has earned a
        reputation for increasing business growth and profitability throughout the global staffing
        market. 100% configurable and fully scalable, Twilio manages the entire placement cycle and
        is chosen by leading recruitment organisations including Hays,
        Adecco and Michael Page.
    </Paragraph>;
