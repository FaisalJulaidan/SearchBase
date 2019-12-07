import React, { useState } from 'react';
import { Typography, Input, Icon, Button, Form, Select } from 'antd';
import { getLink } from '../../../../../helpers';

const { Title, Paragraph, Text } = Typography;

export const BullhornFormItems = ({
                                      FormItem,
                                      layout,
                                      getFieldDecorator,
                                      marketplace,
                                      connectMarketplace,
                                      isConnecting,
                                      isTesting
                                  }) =>
    <>
        {
            marketplace.status !== 'CONNECTED' &&
            marketplace.status !== 'FAILED' &&
            <div>
                <FormItem label="API Username"
                          {...layout}>
                    {getFieldDecorator('username', {
                        rules: [{
                            required: true,
                            message: 'API Username is required'
                        }]
                    })(
                        // To readOnly to avoid autocomplete
                        <Input readOnly
                               onFocus={elem => elem.target.removeAttribute('readonly')}
                               placeholder={'Login of user to use for authentication'}/>
                    )}
                </FormItem>

                <FormItem label="API Password"
                          {...layout}>
                    {getFieldDecorator('password', {

                        rules: [{
                            required: true,
                            max: 32,
                            message: 'API Password is required, and should be less than or 32 character'
                        }]
                    })(
                        // To readOnly to avoid autocomplete
                        <Input readOnly
                               onFocus={elem => elem.target.removeAttribute('readonly')}
                               prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }}/>}
                               placeholder={'User\'s password'} type="password"/>
                    )}
                </FormItem>

                {
                    marketplace.status === 'NOT_CONNECTED' &&
                    <Button type="primary" disabled={isConnecting || isTesting}
                            onClick={connectMarketplace}>Connect</Button>
                }
            </div>
        }

        {
            marketplace.status === 'CONNECTED' &&
            <div style={{ textAlign: 'center' }}>
                <img src={getLink('/static/images/undraw/success.svg')} alt="" height={300}/>
                <Typography.Title>
                    {marketplace.type} is connected
                </Typography.Title>
            </div>
        }

        {
            marketplace.status === 'FAILED' &&
            <div style={{ textAlign: 'center' }}>
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

export const BullhornFeatures = () =>
    <Typography style={{ padding: '0 60px' }}>
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
            <Text code style={{ margin: '0 0 0 5px' }}>
                <a href="https://www.bullhorn.com/uk/technical-support-2/" target={'_blank'}
                   style={{ cursor: 'pointer' }}>
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
                          href={'mailto:info@thesearchbase.com'}
                          style={{ cursor: 'pointer' }}>
                info@thesearchbase.com
            </a></Text>.
        </Paragraph>
    </Typography>;

export const BullhornHeader = () =>
    <Paragraph type="secondary">
        Bullhorn is a cloud computing company headquartered in Boston, Massachusetts. The company provides customer
        relationship management, applicant tracking system and operations software for the staffing industry.
    </Paragraph>;

export const BullhornConnections = ({ getFieldDecorator, crmAP, save, CRMAPList, connectionStatus }) => {
    let [crmID, setCRMID] = useState(crmAP?.ID);
    return (<Form layout='vertical' wrapperCol={{ span: 15 }} style={{ width: '100%' }}>
        <h2>Connect to a CRM Autopilot</h2>
        <Form.Item label="Autopilot selection">
            {getFieldDecorator('AutopilotID', {
                initialValue: crmAP?.ID || null,
                rules: [{ required: false }]
            })(
                <Select disabled={connectionStatus === 'NOT_CONNECTED'} onChange={e => setCRMID(e)}>
                    <Select.Option value={null}>None</Select.Option>
                    {CRMAPList.map(item => {
                        return (<Select.Option value={item.ID}>{item.Name}</Select.Option>);
                    })}
                </Select>
            )}
            <Button disabled={connectionStatus === 'NOT_CONNECTED'} type={'primary'} size={'large'}
                    style={{ marginTop: 30 }} onClick={() => save('Bullhorn', crmID)}>
                Save changes
            </Button>
        </Form.Item>
    </Form>);
};