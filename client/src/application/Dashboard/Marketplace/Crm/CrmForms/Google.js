import React from 'react';
import {Button, Col, Icon, Input, Popconfirm, Typography} from "antd";
import styles from "../Crm.module.less";
import {getLink} from "helpers";

const {Title, Paragraph, Text} = Typography;

//api/calendar/google/authorize
const loginWithGoogle = (clientID, responseType, scope, redirectURI) => {
    return (<a href={`https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientID}&response_type=${responseType}&scope=${scope}&redirect_uri=${redirectURI}&access_type=offline`}>
        <img src={"https://developers.google.com/identity/images/btn_google_signin_light_normal_web.png"} />
    </a>)
}



export const GoogleFormItems = ({
                                      FormItem,
                                      layout,
                                      getFieldDecorator,
                                      CRM,
                                      disconnectCRM,
                                      connectCRM,
                                      testCRM,
                                      isConnecting,
                                      isTesting,
                                      isDisconnecting
                                  }) =>
    <div>
        {
            CRM.status !== "CONNECTED" &&
            CRM.status !== "FAILED" &&
            <div>
                {loginWithGoogle("623652835897-tj9rf1v6hd1tak5bv5hr4bq9hrvjns95.apps.googleusercontent.com",
                                    "code",
                                    "https://www.googleapis.com/auth/calendar.events",
                                    "http://localhost:3000/dashboard/marketplace?googleVerification=true")}
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
                        title="Chatbot conversations will no longer be synced with Bullhorn account"
                        onConfirm={disconnectCRM}
                        okType={'danger'}
                        okText="Disconnect"
                        cancelText="No"
                    >
                        <Button type="danger" disabled={isDisconnecting}>Disconnect</Button>
                    </Popconfirm>
                }

            </div>
        </Col>

    </div>;

export const GoogleFeatures = () =>
    <Typography style={{padding: '0 60px'}}>
        <Title>Introduction</Title>
        <Paragraph>
            We currently offer a full all-round integration with Bullhorn. You can simply login with your Bullhorn
            credentials and we will read and write all of data processed by our platform and the chatbots that you have
            created.
        </Paragraph>

        <Paragraph>
            For your integration to start, you will need to request some information from Bullhorn.
            What you’ll need:
            <ul>
                <li>Username</li>
                <li>Password</li>
            </ul>
        </Paragraph>
        <Paragraph>
            You can request both information by heading to this link:
            <Text code style={{margin: '0 0 0 5px'}}>
                <a href="https://www.bullhorn.com/uk/technical-support-2/" target={'_blank'}
                   style={{cursor: 'pointer'}}>
                    https://www.bullhorn.com/uk/technical-support-2/
                </a>
            </Text>.
        </Paragraph>

        <Paragraph>
            Once you have the necessary information, you can simply start using Bullhorn + TheSearchBase.
        </Paragraph>

        <Title level={2}>Guidelines and Resources</Title>
        <Paragraph>
            You can request more information about our Bullhorn CRM integration by emailing us at:
            <Text code><a target={'_blank'}
                          href={"mailto:info@thesearchbase.com"}
                          style={{cursor: 'pointer'}}>
                info@thesearchbase.com
            </a></Text>.
        </Paragraph>
    </Typography>;

export const GoogleHeader = () =>
    <Paragraph type="secondary">
        Bullhorn is a cloud computing company headquartered in Boston, Massachusetts. The company provides customer
        relationship management, applicant tracking system and operations software for the staffing industry.
    </Paragraph>;


