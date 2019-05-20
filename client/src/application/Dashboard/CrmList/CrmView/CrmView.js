import React from 'react'
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Avatar, Breadcrumb, Form, Modal, Tabs, Typography} from 'antd';
import styles from './CrmView.module.less'
import {history} from "helpers";
import 'types/CRM_Types';
import AdaptFormItems from "./CrmForms/Adapt";
import BullhornFormItems from "./CrmForms/Bullhorn";
import VincereFormItems from "./CrmForms/Vincere";
import {connect} from 'react-redux';
import {crmActions} from "store/actions";

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
                history.push('/dashboard/crmlist')
        });
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.connectedCRM_ID)
            this.setState({
                CRM: {
                    ...this.state.CRM,
                    ID: nextProps.connectedCRM_ID,
                    status: 'CONNECTED'
                }
            });

        if (nextProps.connectedCRM_ID === "disconnect")
            this.setState({
                CRM: {
                    ...this.state.CRM,
                    ID: null,
                    status: 'DISCONNECTED'
                }
            });
    }

    connectCRM = () => this.props.form.validateFields((err, values) => {
        if (err) return;
        this.props.dispatch(
            crmActions.connectCrm(
                {
                    type: this.state.CRM.type,
                    auth: {...values}
                }
            )
        );
    });

    testCRM = () => this.props.form.validateFields(async (err, values) => {
        if (err) return;
        this.props.dispatch(
            crmActions.testCrm(
                {
                    type: this.state.CRM.type,
                    auth: {...values}
                }
            )
        );
    });

    disconnectCRM = () => {
        const {/**{CRM}*/CRM} = this.state;
        confirm({
            title: `Disconnect from ${CRM.type}`,
            content: <p>Chatbot conversations will no longer be synced with {CRM.type} account</p>,
            onOk: () => {
                this.props.dispatch(
                    crmActions.disconnectCrm(
                        {
                            ID: this.state.CRM.ID,
                        }
                    )
                )
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
                            Bond Adapt, specialist portfolio of recruitment software applications has earned a
                            reputation for increasing business growth and profitability throughout the global staffing
                            market. 100% configurable and fully scalable, Adapt manages the entire placement cycle and
                            is chosen by leading recruitment organisations including <Text code>Hays</Text>,
                            <Text code>Adecco</Text> and <Text code>Michael Page</Text> .
                        </Paragraph>
                    </div>
                </div>

                <div className={styles.Body}>
                    <Breadcrumb>
                        <Breadcrumb.Item>
                            <a href={"javascript:void(0);"}
                               onClick={() => history.push('/dashboard/crmlist')}>
                                CRMs List
                            </a>
                        </Breadcrumb.Item>
                        <Breadcrumb.Item>{CRM.type}</Breadcrumb.Item>
                    </Breadcrumb>
                    <br/>
                    <Tabs defaultActiveKey="1">
                        <TabPane tab="Feature" key="1">
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
                                        <li>
                                            Adapt Domain
                                        </li>
                                        <li>
                                            Username
                                        </li>
                                        <li>
                                            Password
                                        </li>
                                        <li>
                                            Profile
                                        </li>
                                        <li>
                                            Locale
                                        </li>
                                        <li>
                                            (Location e.g. en_GB, en_US)
                                        </li>
                                        <li>
                                            Timezone (e.g. GMT)
                                        </li>
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

function

mapStateToProps(state) {
    return {
        connectedCRM_ID: state.crm.connectedCRM_ID,
    };
}

export default connect(mapStateToProps)(Form.create()(CrmView));

