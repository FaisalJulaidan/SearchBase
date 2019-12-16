import React from 'react';
import {Button, Icon, Input, Select, Typography} from "antd";
import {getLink} from "helpers";

const {Option} = Select;
const {Title, Paragraph, Text} = Typography;

export const AdaptFormItems = ({
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
                <FormItem label="Domain"
                          {...layout}>
                    {getFieldDecorator('domain', {
                        rules: [{
                            required: true,
                            message: "Please add your domain name",
                        }],
                    })(
                        <Input placeholder={'Your Domain'}/>
                    )}
                </FormItem>

                <FormItem label="Username"
                          {...layout}>
                    {getFieldDecorator('username', {
                        rules: [{
                            required: true,
                            max: 20,
                            message: "Username is required, and should be less than or 20 character",
                        }],
                    })(
                        // To readOnly to avoid autocomplete
                        <Input readOnly
                               onFocus={elem => elem.target.removeAttribute('readonly')}
                               placeholder={'Login of user to use for authentication'}/>
                    )}
                </FormItem>

                <FormItem label="Password"
                          {...layout}>
                    {getFieldDecorator('password', {

                        rules: [{
                            required: true,
                            max: 32,
                            message: "Password is required, and should be less than or 32 character",
                        }],
                    })(
                        // To readOnly to avoid autocomplete
                        <Input readOnly
                               onFocus={elem => elem.target.removeAttribute('readonly')}
                               prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                               placeholder={"User's password"} type="password"/>
                    )}
                </FormItem>

                <FormItem label="Profile"
                          {...layout}>
                    {getFieldDecorator('profile', {
                        rules: [{
                            required: true,
                            message: "Profile is required field",
                        }],
                    })(
                        <Input placeholder={"Profile to use (e.g. CoreProfile)"}/>
                    )}
                </FormItem>

                <FormItem label="Locale" {...layout}>
                    {getFieldDecorator('locale', {
                        rules: [{
                            required: true,
                            message: "Locale is required field",
                        }],
                    })(
                        <Input placeholder={"Locale is like: en_GB"}/>
                    )}
                </FormItem>

                <FormItem label="Timezone"
                          {...layout}>
                    {getFieldDecorator('timezone', {
                        rules: [{
                            required: true,
                            message: "Timezone is required field",
                        }],
                    })(
                        <Input placeholder={"Time zone identifier (e.g. GMT)"}/>
                    )}
                </FormItem>

                <FormItem label="Date Format"
                          {...layout}>
                    {getFieldDecorator('dateFormat', {
                        initialValue: 0,
                        rules: [{
                            required: true,
                            message: "Date Format is required field",
                        }],
                    })(
                        <Select placeholder={'Select one of the Date Formats'}>
                            <Option value="0">0 – default</Option>
                            <Option value="1">1 – Long</Option>
                            <Option value="2">2 – Medium</Option>
                            <Option value="3">3 – Short</Option>
                        </Select>
                    )}
                </FormItem>


                <FormItem label="Time Format"
                          {...layout}>
                    {getFieldDecorator('timeFormat', {
                        initialValue: 0,
                        rules: [{
                            required: true,
                            message: "Time Format is required field",
                        }],
                    })(
                        <Select placeholder={'Select one of the Time Formats'}>
                            <Option value="0">0 – Full</Option>
                            <Option value="1">1 – Long</Option>
                            <Option value="2">2 – Medium</Option>
                            <Option value="3">3 – Short</Option>
                        </Select>
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

export const AdaptFeatures = ({}) =>
    <Typography style={{padding: '0 60px'}}>
        <Title>Introduction</Title>
        <Paragraph>
            Adapt users can very simply benefit from using their systems directly by logging in
            through our software to connect their CRM to our platform.
        </Paragraph>
        <Paragraph>
            Once you have the required information and have successfully logged in – you are all
            done.
        </Paragraph>
        <Paragraph>
            What you’ll need:
            <ul>
                <li>Adapt Domain</li>
                <li>Username</li>
                <li>Password</li>
                <li>Profile</li>
                <li>Locale</li>
                <li>(Location e.g. en_GB, en_US)</li>
                <li>Timezone (e.g. GMT)</li>
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

export const AdaptHeader = () =>
    <Paragraph type="secondary">
        Bond Adapt, specialist portfolio of recruitment software applications has earned a
        reputation for increasing business growth and profitability throughout the global staffing
        market. 100% configurable and fully scalable, Adapt manages the entire placement cycle and
        is chosen by leading recruitment organisations including Hays,
        Adecco and Michael Page.
    </Paragraph>;
