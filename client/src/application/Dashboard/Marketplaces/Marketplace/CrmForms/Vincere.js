import React from 'react';
import {Button, Col, Popconfirm, Typography} from "antd";
import styles from "../../Crm/Crm.module.less";
import {getLink} from "helpers";

const {Title, Paragraph, Text} = Typography;

export const VincereFormItems = ({
                                     FormItem,
                                     layout,
                                     getFieldDecorator,
                                     marketplace,
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
            marketplace.status !== "CONNECTED" &&
            marketplace.status !== "FAILED" &&
            <div>
                <a href="javascript:void(0);" name="Connect Vincere Account" title=" Vincere Connection "
                   onClick={() => {
                       return window.open("https://id.vincere.io/oauth2/authorize?client_id=9829f4ad-3ff3-4d00-8ecf-e5d7fa2983d1&response_type=code&redirect_uri=https://www.thesearchbase.com/api/marketplace_callback&state=%7B%22type%22%3A%22Vincere%22%2C%22companyID%22%3A%22"+companyID+"%22%7D", "Ratting", "width=600,height=400,0,top=40%,right=30%,status=0,")
                   }}>Click here</a>


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
                    {marketplace.type} is failing this is usually not from us, please contact the CRM provider
                </Paragraph>
            </div>
        }


    </div>;

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


