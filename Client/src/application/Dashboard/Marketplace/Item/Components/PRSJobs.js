import React from 'react';
import {Typography} from "antd";

const {Title, Paragraph, Text} = Typography;

export const PRSJobsFeatures = () =>
    <Typography style={{padding: '0 60px'}}>
        <Title>Introduction</Title>
        <Paragraph>
            We currently offer a full all-round integration with PRSJobs. You can simply login with your PRSJobs
            credentials and we will read and write all of data processed by our platform and the chatbots that you have
            created.
        </Paragraph>

        <Paragraph>
            For your integration to start, you will need to request some information from PRSJobs.
            What you’ll need:
            <ul>
                <li>Username</li>
                <li>Password</li>
            </ul>
        </Paragraph>
        <Paragraph>
            You can request both information by heading to this link:
            <Text code style={{margin: '0 0 0 5px'}}>
                <a href="https://www.PRSJobs.com/uk/technical-support-2/" target={'_blank'}
                   style={{cursor: 'pointer'}}>
                    https://www.PRSJobs.com/uk/technical-support-2/
                </a>
            </Text>.
        </Paragraph>

        <Paragraph>
            Once you have the necessary information, you can simply start using PRSJobs + TheSearchBase.
        </Paragraph>

        <Title level={2}>Guidelines and Resources</Title>
        <Paragraph>
            You can request more information about our PRSJobs CRM integration by emailing us at:
            <Text code><a target={'_blank'}
                          href={"mailto:info@thesearchbase.com"}
                          style={{cursor: 'pointer'}}>
                info@thesearchbase.com
            </a></Text>.
        </Paragraph>
    </Typography>;

export const PRSJobsHeader = () =>
    <Paragraph type="secondary">
        PRSJobs description
    </Paragraph>;


