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

                <FormItem label="Notify Service SID"
                          {...layout}>
                    {getFieldDecorator('notify_service_sid', {
                        rules: [{
                            required: true,
                            message: "Please add your Notify Service SID",
                        }],
                    })(
                        <Input placeholder={'Starting IS...'}/>
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
            What you’ll need:
            <ul>
                <li><b>Account SID</b></li>
                <li><b>Notify Service SID</b></li>
                <li><b>Auth Token</b></li>
            </ul>
        </Paragraph>
        <Paragraph>
            How to procure them on the Twilio website:
            <ul>
                <li>
                    <h5>Account SID & Auth Token</h5>
                    Once you login into your Twilio account you will be presented with your 'Console' page. On it you
                    will be able to see your Account SID and also reveal your Auth Token.
                </li>
                <li>
                    <h5>Notify Service SID</h5>
                    First you'll need to get yourself a number. If you have one already simply skip this step. Once
                    logged in click on the search box on the top right and type in "Number". Press on "Buy a Number" and
                    you will be presented with a filtering menu. Simply filter for your desired number and follow the
                    instructions on buying however make sure that your number has SMS enabled or else you will not be
                    able to use it with us.<br/><br/>
                    Now that you have a number click on "Programmable SMS" from the far left menu on your screen. Next
                    go to "SMS" from the new menu that appeared on the left and click on the big + to create a new
                    Messaging Service. Give it a name you like and for Use Case put "Notifications, Outbound Only". You
                    will now be presented with the Settings page which you can leave as it is.<br/><br/>
                    You now have a Number and a Messaging Service. To be able to use the Messaging Service you will need
                    to give it the number. To do that click on "Numbers" in the "Programmable SMS" menu on your left.
                    Click on "Add an Existing Number", select the number you created and press on Add Selected. Finally
                    press on "Back" from the menu if you are still inside the Messaging Service. You will be presented
                    with your Messaging Service SID in the list of messaging services on your screen.<br/><br/>
                    Finally go to the search bar on the top right again, type in "Notify" and press on "Notify
                    Services". Add a new service by pressing the plus sign and giving it a name you like. Go inside the
                    service you just created and connect your Messaging Service under the "Messaging Service SID"
                    dropdown. Your Notify Service has not been completed and you can use its SID.
                </li>
            </ul>
        </Paragraph>
    </Typography>;

export const TwilioHeader = () =>
    <Paragraph type="secondary">
        Twilio two-way SMS and MMS messages allow you to carry on a conversation by both sending and receiving text and
        multimedia messages. You can integrate all of your Chatbots to natively reach your Talent Pools, Clients and
        candidates from within SearchBase.
    </Paragraph>;
