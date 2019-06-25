import React from 'react';
import {Button, Popconfirm, Typography} from "antd";
import {getLink} from "helpers";

const {Title, Paragraph, Text} = Typography;

export const BullhornButton = ({type, companyID, status, disconnectMarketplace, isDisconnecting}) =>
    <>
        {
            status !== "CONNECTED" &&
            status !== "FAILED" &&
            <>
                {
                    status === "NOT_CONNECTED" &&
                    <>
                        <Button type="primary"
                        icon={'login'}
                        style={{width: 'auto'}}
                        onClick={() => {
                        return window.open("https://auth.bullhornstaffing.com/oauth/authorize?response_type=code&redirect_uri=https://www.thesearchbase.com/api/bullhorn_callback&client_id=7719607b-7fe7-4715-b723-809cc57e2714&state={\"type\":\"Bullhorn\",\"companyID\":\"" + companyID + "\"}", "Ratting", "width=600,height=600,0,top=40%,right=30%,status=0,")
                        }} size={'large'}>Connect Bullhorn</Button>
                    </>
                }
            </>
        }
        {
            (status === "CONNECTED" || status === "FAILED")
            &&
            <Popconfirm placement={'bottomRight'}
                        title="Chatbot conversations will no longer be synced with Bullhorn account"
                        onConfirm={disconnectMarketplace}
                        okType={'danger'}
                        okText="Disconnect"
                        cancelText="No">
                <Button type="danger"
                        style={{width: 'auto'}}
                        size={'large'}
                        disabled={isDisconnecting}>
                    {
                        status === "FAILED" ? '(Failed) click to disconnect' : 'Disconnect'
                    }
                </Button>
            </Popconfirm>
        }
    </>;

export const BullhornFeatures = () =>
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

export const BullhornHeader = () =>
    <Paragraph type="secondary">
        Bullhorn is a cloud computing company headquartered in Boston, Massachusetts. The company provides customer
        relationship management, applicant tracking system and operations software for the staffing industry.
    </Paragraph>;


