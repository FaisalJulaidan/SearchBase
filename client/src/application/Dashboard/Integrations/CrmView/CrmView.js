import React from 'react'
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Typography, Avatar, Tabs, Breadcrumb, Form, Modal, Col, Button, Icon} from 'antd';


import styles from './CrmView.module.less'
import {history} from "helpers";
import 'types/CRM_Types';
import AdaptFormItems from "./CrmForms/Adapt";
import BullhornFormItems from "./CrmForms/Bullhorn";
import VincereFormItems from "./CrmForms/Vincere";

const TabPane = Tabs.TabPane;
const {Title, Paragraph, Text} = Typography;
const FormItem = Form.Item;

const confirm = Modal.confirm;

class CrmView extends React.Component {

    state = {
        /** @type {CRM} */
        CRM: {}
    };

    componentDidMount() {
        this.setState({
            ...this.props.location?.state
        }, () => {
            // If the state is not passed from the parent page redirect the user to integration page to
            // click on the needed CRM to show its data (or use its state)
            if (!this.state.CRM?.type)
                history.push('/dashboard/integrations')
        });
    }


    connectCRM = () => this.props.form.validateFields((err, values) => {
        const {/** @type {CRM} */CRM} = this.state;
        console.log(values)
        // if (!err)
        //     this.props.dispatch(assistantActions.connectCRM(
        //         {
        //             type: CRM.type,
        //             auth: {...values},
        //         }, this.props.assistant));

    });

    testCRM = () => this.props.form.validateFields((err, values) => {
        console.log(values)
        // if (!err)
        //     this.props.dispatch(assistantActions.testCRM(
        //         {
        //             type: CRM.type,
        //             auth: {...values},
        //         }, this.props.assistant));

    });

    disconnectCRM = () => {
        const {/**{CRM}*/CRM} = this.state;
        confirm({
            title: `Disconnect from ${CRM.type}`,
            content: <p>Chatbot conversations will no longer be synced with {CRM.type} account</p>,
            onOk: () => {
                // this.props.dispatch(assistantActions.disconnectCRM({
                //     Type: CRM.type
                // }, this.props.assistant));
            }
        });
    };


    render() {
        const {getFieldDecorator} = this.props.form;
        const layout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };

        const {/**{CRM}*/CRM} = this.state;
        return (
            <NoHeaderPanel>
                <div className={styles.Title}>
                    <Avatar shape="square" size={80}
                            src={this.state.CRM.image}
                            className={styles.Avatar}/>
                    <div className={styles.DetailsWithAvatar}>
                        <Title level={2}>{this.state.CRM?.type}</Title>
                        <Paragraph type="secondary">
                            We supply a series of design principles, practical patterns and high quality design
                            resources
                            (<Text code>Sketch</Text> and <Text code>Axure</Text>), to help people create their
                            product
                            prototypes beautifully and efficiently.
                        </Paragraph>
                    </div>
                </div>

                <div className={styles.Body}>
                    <Breadcrumb>
                        <Breadcrumb.Item>
                            <a href={"javascript:void(0);"}
                               onClick={() => history.push('/dashboard/integrations')}>
                                Integrations
                            </a>
                        </Breadcrumb.Item>
                        <Breadcrumb.Item>{CRM.type}</Breadcrumb.Item>
                    </Breadcrumb>
                    <br/>
                    <Tabs defaultActiveKey="2">
                        <TabPane tab="Feature" key="1">
                            <Typography style={{
                                padding: '0 60px'
                            }}>
                                <Title>Introduction</Title>
                                <Paragraph>
                                    In the process of internal desktop applications development, many different design
                                    specs and
                                    implementations would be involved, which might cause designers and developers
                                    difficulties and
                                    duplication and reduce the efficiency of development.
                                </Paragraph>
                                <Paragraph>
                                    After massive project practice and summaries, Ant Design, a design language for
                                    background
                                    applications, is refined by Ant UED Team, which aims to{' '}
                                    <Text strong>
                                        uniform the user interface specs for internal background projects, lower the
                                        unnecessary
                                        cost of design differences and implementation and liberate the resources of
                                        design and
                                        front-end development
                                    </Text>
                                </Paragraph>
                                <Title level={2}>Guidelines and Resources</Title>
                                <Paragraph>
                                    We supply a series of design principles, practical patterns and high quality design
                                    resources
                                    (<Text code>Sketch</Text> and <Text code>Axure</Text>), to help people create their
                                    product
                                    prototypes beautifully and efficiently.
                                </Paragraph>

                                <Paragraph>
                                    <ul>
                                        <li>
                                            <a href="/docs/spec/proximity">Principles</a>
                                        </li>
                                        <li>
                                            <a href="/docs/pattern/navigation">Patterns</a>
                                        </li>
                                        <li>
                                            <a href="/docs/resource/download">Resource Download</a>
                                        </li>
                                    </ul>
                                </Paragraph>
                            </Typography>
                        </TabPane>

                        <TabPane tab="Connection" key="2" style={{
                            padding: '0 60px'
                        }}>
                            <Form layout='horizontal'>

                                {
                                    CRM.type === "Adapt" &&
                                    <AdaptFormItems getFieldDecorator={getFieldDecorator}
                                                    layout={layout}
                                                    FormItem={FormItem}
                                                    CRM={CRM}
                                                    disconnectCRM={this.disconnectCRM}
                                                    connectCRM={this.connectCRM}
                                                    testCRM={this.testCRM}/>

                                }


                                {
                                    CRM.type === "Bullhorn" &&
                                    <BullhornFormItems getFieldDecorator={getFieldDecorator}
                                                       layout={layout}
                                                       FormItem={FormItem}
                                                       CRM={CRM}
                                                       disconnectCRM={this.disconnectCRM}
                                                       connectCRM={this.connectCRM}
                                                       testCRM={this.testCRM}/>

                                }

                                {
                                    CRM.type === "Vincere" &&
                                    <VincereFormItems getFieldDecorator={getFieldDecorator}
                                                      layout={layout}
                                                      FormItem={FormItem}
                                                      CRM={CRM}
                                                      disconnectCRM={this.disconnectCRM}
                                                      connectCRM={this.connectCRM}
                                                      testCRM={this.testCRM}/>

                                }

                            </Form>
                        </TabPane>
                    </Tabs>

                </div>

            </NoHeaderPanel>
        );
    }
}

export default Form.create()(CrmView);

