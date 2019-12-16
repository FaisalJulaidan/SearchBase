import React from 'react';
import {Button, Icon, Input, Typography} from "antd";
import {getLink} from "helpers";

const {Title, Paragraph, Text} = Typography;

export const GreenhouseFormItem = ({
                                       FormItem,
                                       layout,
                                       getFieldDecorator,
                                       marketplace,
                                       disconnectMarketplace,
                                       connectMarketplace,
                                       isConnecting,
                                       isTesting,
                                   }) =>
    <div>
        {
            marketplace.status !== "CONNECTED" &&
            marketplace.status !== "FAILED" &&
            <div>
                <FormItem label="User ID"
                          {...layout}>
                    {getFieldDecorator('user_id', {
                        rules: [{
                            required: true,
                            message: "User ID is required",
                        }],
                    })(
                        // To readOnly to avoid autocomplete
                        <Input readOnly
                               onFocus={elem => elem.target.removeAttribute('readonly')}
                               prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder={"User ID"} type="password"/>
                    )}
                </FormItem>

                <FormItem label="API Key"
                          {...layout}>
                    {getFieldDecorator('api_key', {
                        rules: [{
                            required: true,
                            message: "API key is required",
                        }],
                    })(
                        // To readOnly to avoid autocomplete
                        <Input readOnly
                               onFocus={elem => elem.target.removeAttribute('readonly')}
                               prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder={"API Key"} type="password"/>
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
                <img src={"/images/undraw/success.svg"} alt="" height={300}/>
                <Typography.Title>
                    {marketplace.type} is connected
                </Typography.Title>
            </div>
        }

        {
            marketplace.status === "FAILED" &&
            <div style={{textAlign: 'center'}}>
                <img src={"/images/undraw/failed.svg"} alt="" height={300}/>
                <Title>
                    {marketplace.type} is failed
                </Title>
                <Paragraph type="secondary">
                    {marketplace.type} is failing this is usually not from us, please contact the CRM provider
                </Paragraph>
            </div>
        }
    </div>;

export const GreenhouseFeatures = () =>
    <Typography style={{padding: '0 60px'}}>
        <Title>Introduction</Title>
        <Paragraph>
            With Greenhouse Recruiting, hiring finally becomes a strategic driver of your business, removing
            administrative burden and keeping you in the lead.
        </Paragraph>

        <Paragraph>
            For your integration to start, you will need to request some information from Greenhouse.
            What you’ll need:
            <ul>
                <li>Api Key</li>
            </ul>
        </Paragraph>

        {/*<Paragraph>*/}
        {/*You can request both information by heading to this link:*/}
        {/*<Text code style={{margin: '0 0 0 5px'}}>*/}
        {/*<a href="https://www.bullhorn.com/uk/technical-support-2/" target={'_blank'}*/}
        {/*style={{cursor: 'pointer'}}>*/}
        {/*https://www.bullhorn.com/uk/technical-support-2/*/}
        {/*</a>*/}
        {/*</Text>.*/}
        {/*</Paragraph>*/}

        <Paragraph>
            Once you have the necessary information, you can simply start using Greenhouse + TheSearchBase.
        </Paragraph>

        <Title level={2}>Guidelines and Resources</Title>
        <Paragraph>
            You can request more information about our Greenhouse CRM integration by emailing us at:
            <Text code><a target={'_blank'}
                          href={"mailto:info@thesearchbase.com"}
                          style={{cursor: 'pointer'}}>
                info@thesearchbase.com
            </a></Text>.
        </Paragraph>
    </Typography>;

export const GreenhouseHeader = () =>
    <Paragraph type="secondary">
        Greenhouse works seamlessly with over 220 partners and third-party apps and technologies, enabling you to solve
        specific problems without ever leaving the platform.
    </Paragraph>;


