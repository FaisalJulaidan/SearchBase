import React from 'react';
import {Button, Col, Icon, Input, Popconfirm, Typography} from "antd";
import styles from "../Crm.module.less";
import {getLink} from "helpers";

const {Title, Paragraph, Text} = Typography;

export const OutlookFormItems = ({
                                      FormItem,
                                      layout,
                                      getFieldDecorator,
                                      CRM,
                                      disconnectCRM,
                                      connectCRM,
                                      testCRM,
                                      isConnecting,
                                      isTesting,
                                      isDisconnecting,
                                        companyID
                                  }) =>
    <div>
        {
            CRM.status !== "CONNECTED" &&
            CRM.status !== "FAILED" &&
            <div>
                {/*<a href={"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=0978960c-c837-479f-97ef-a75be4bbacd4&redirect_uri=https://www.thesearchbase.com/crm_callback&scope=openid+Calendars.ReadWrite"} target="_blank">Click me</a>*/}
                <a href="javascript:void(0);" NAME="Connect Outlook Account"  title=" Outlook Connection " onClick={() => {return window.open("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=0978960c-c837-479f-97ef-a75be4bbacd4&redirect_uri=https://www.thesearchbase.com/api/outlook_callback&scope=openid+Calendars.ReadWrite+offline_access&state="+companyID,"Ratting","width=600,height=400,0,top=40%,right=30%,status=0,")}}>Click here</a>
            </div>
        }

        {
            CRM.status === "CONNECTED" &&
            <div style={{textAlign: 'center'}}>
                <img src={getLink('/static/images/undraw/success.svg')} alt="" height={300}/>
                <Typography.Title>
                    {CRM.type} is connected
                </Typography.Title>
            </div>
        }

        {
            CRM.status === "FAILED" &&
            <div style={{textAlign: 'center'}}>
                <img src={getLink('/static/images/undraw/failed.svg')} alt="" height={300}/>
                <Title>
                    {CRM.type} is failed
                </Title>
                <Paragraph type="secondary">
                    {CRM.type} is failing this is usually not from us, please contact the CRM provider
                </Paragraph>
            </div>
        }

        <Col span={16} offset={4}>
            <div className={styles.Buttons}>
                {
                    (CRM.status === "CONNECTED" || CRM.status === "FAILED")
                    &&
                    <Popconfirm
                        title="Chatbot conversations will no longer be synced with Outlook account"
                        onConfirm={disconnectCRM}
                        okType={'danger'}
                        okText="Disconnect"
                        cancelText="No"
                    >
                        <Button type="danger" disabled={isDisconnecting}>Disconnect</Button>
                    </Popconfirm>
                }

                {
                    CRM.status === "NOT_CONNECTED" &&
                    <>
                        <Button type="primary" disabled={isConnecting || isTesting}
                                onClick={connectCRM}>Connect</Button>
                        <Button onClick={testCRM} disabled={isConnecting || isTesting}>Test</Button>
                    </>
                }
            </div>
        </Col>

    </div>;

export const OutlookFeatures = () =>
    <Typography style={{padding: '0 60px'}}>
        <Title>Introduction</Title>
        <Paragraph>
            We currently offer a full all-round integration with Outlook. You can simply login with your Outlook
            credentials and we will read and write all of data processed by our platform and the chatbots that you have
            created.
        </Paragraph>

        <Paragraph>
            For your integration to start, you will need to request some information from Outlook.
            What you’ll need:
            <ul>
                <li>Username</li>
                <li>Password</li>
            </ul>
        </Paragraph>
        <Paragraph>
            You can request both information by heading to this link:
            <Text code style={{margin: '0 0 0 5px'}}>
                <a href="https://www.Outlook.com/uk/technical-support-2/" target={'_blank'}
                   style={{cursor: 'pointer'}}>
                    https://www.Outlook.com/uk/technical-support-2/
                </a>
            </Text>.
        </Paragraph>

        <Paragraph>
            Once you have the necessary information, you can simply start using Outlook + TheSearchBase.
        </Paragraph>

        <Title level={2}>Guidelines and Resources</Title>
        <Paragraph>
            You can request more information about our Outlook CRM integration by emailing us at:
            <Text code><a target={'_blank'}
                          href={"mailto:info@thesearchbase.com"}
                          style={{cursor: 'pointer'}}>
                info@thesearchbase.com
            </a></Text>.
        </Paragraph>
    </Typography>;

export const OutlookHeader = () =>
    <Paragraph type="secondary">
        Outlook description
    </Paragraph>;


