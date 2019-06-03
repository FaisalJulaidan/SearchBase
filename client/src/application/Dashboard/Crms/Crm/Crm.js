import React from 'react'
import {history} from "helpers";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Avatar, Breadcrumb, Button, Form, Modal, Tabs, Typography} from 'antd';
import styles from './Crm.module.less'
import 'types/CRM_Types';
import {AdaptFeatures, AdaptFormItems, AdaptHeader} from "./CrmForms/Adapt";
import {BullhornFeatures, BullhornFormItems, BullhornHeader} from "./CrmForms/Bullhorn";
import VincereFormItems from "./CrmForms/Vincere";
import {connect} from 'react-redux';
import {crmActions} from "store/actions";
import {CSVLink} from "react-csv";

const TabPane = Tabs.TabPane;
const {Title} = Typography;
const FormItem = Form.Item;

const confirm = Modal.confirm;

class Crm extends React.Component {

    componentWillMount() {
        if (!this.props.location.state)
            return history.push('/dashboard/crmlist');
        const /** @type {CRM}*/crm = this.props.location.state?.crm || {};
        this.props.dispatch(crmActions.exportRecruiterValueReport({Name: crm.type}))
    }

    componentWillReceiveProps(nextProps) {
        const /** @type {CRM}*/crm = this.props.location.state?.crm || {};
        const index = nextProps.CRMsList.findIndex(serverCRM => serverCRM.Type === crm.type);
        if (index === -1) {
            // if there is not crm from the server
            crm.status = 'NOT_CONNECTED';
            delete crm.ID;
        } else {
            // if there is a crm, check if it is failed or connected
            // and add the ID
            crm.status = nextProps.CRMsList[index].Status ? "CONNECTED" : "FAILED";
            crm.ID = nextProps.CRMsList[index].ID;
        }
        if(nextProps.exportData){
            crm.exportData = nextProps.exportData;
        }
    }

    connectCRM = () => this.props.form.validateFields((err, values) => {
        if (err) return;
        const /** @type {CRM}*/crm = this.props.location.state?.crm || {};
        this.props.dispatch(
            crmActions.connectCrm(
                {
                    type: crm.type,
                    auth: {...values}
                }
            )
        );
    });

    testCRM = () => this.props.form.validateFields((err, values) => {
        if (err) return;
        const /** @type {CRM}*/crm = this.props.location.state?.crm || {};
        this.props.dispatch(
            crmActions.testCrm(
                {
                    type: crm.type,
                    auth: {...values}
                }
            )
        );
    });

    disconnectCRM = () => {
        const /** @type {CRM}*/crm = this.props.location.state?.crm || {};
        this.props.dispatch(crmActions.disconnectCrm({ID: crm.ID}))
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        const layout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const /** @type {CRM}*/crm = this.props.location.state?.crm || {};
        return (
            <NoHeaderPanel>
                <div className={styles.Title}>
                    <Avatar shape="square" src={crm.image} className={styles.Avatar}/>
                    <div className={styles.DetailsWithAvatar}>
                        <Title level={2}>{crm.type}</Title>
                        {
                            crm.type === "Adapt" &&
                            <AdaptHeader/>
                        }
                        {
                            crm.type === "Bullhorn" &&
                            <BullhornHeader/>
                        }
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
                        <Breadcrumb.Item>{crm.type}</Breadcrumb.Item>
                    </Breadcrumb>

                    {crm.type === "Bullhorn" ? <><br/>
                        <Button className={styles.Panel_Header_Button} type="primary" icon="download"
                                loading={crm.exportData===undefined}>
                            <CSVLink filename={"Recruiter Pipeline Report.csv"} data={crm.exportData || []}
                                     style={{color:"white"}}> Recruiter Pipeline Report</CSVLink>
                        </Button></> : <></>}

                    <br/>

                    <Tabs defaultActiveKey="1">
                        <TabPane tab="Feature" key="1">
                            {
                                crm.type === "Adapt" &&
                                <AdaptFeatures/>
                            }
                            {
                                crm.type === "Bullhorn" &&
                                <BullhornFeatures/>
                            }
                        </TabPane>

                        <TabPane tab="Connection" key="2" style={{
                            padding: '0 60px'
                        }}>
                            <Form layout='horizontal'>

                                {
                                    crm.type === "Adapt" &&
                                    <AdaptFormItems getFieldDecorator={getFieldDecorator}
                                                    layout={layout}
                                                    CRM={crm}
                                                    FormItem={FormItem}
                                                    isConnecting={this.props.isConnecting}
                                                    isTesting={this.props.isTesting}
                                                    isDisconnecting={this.props.isDisconnecting}
                                                    disconnectCRM={this.disconnectCRM}
                                                    connectCRM={this.connectCRM}
                                                    testCRM={this.testCRM}/>

                                }


                                {
                                    crm.type === "Bullhorn" &&
                                    <BullhornFormItems getFieldDecorator={getFieldDecorator}
                                                       layout={layout}
                                                       FormItem={FormItem}
                                                       CRM={crm}
                                                       isConnecting={this.props.isConnecting}
                                                       isTesting={this.props.isTesting}
                                                       isDisconnecting={this.props.isDisconnecting}
                                                       disconnectCRM={this.disconnectCRM}
                                                       connectCRM={this.connectCRM}
                                                       testCRM={this.testCRM}/>

                                }

                                {
                                    crm.type === "Vincere" &&
                                    <VincereFormItems getFieldDecorator={getFieldDecorator}
                                                      layout={layout}
                                                      FormItem={FormItem}
                                                      CRM={crm}
                                                      isConnecting={this.props.isConnecting}
                                                      isTesting={this.props.isTesting}
                                                      isDisconnecting={this.props.isDisconnecting}
                                                      disconnectCRM={this.disconnectCRM}
                                                      connectCRM={this.connectCRM}
                                                      testCRM={this.testCRM}/>

                                }

                            </Form>
                        </TabPane>
                    </Tabs>

                </div>

            </NoHeaderPanel>
        )
    }
}


function mapStateToProps(state) {
    return {
        CRMsList: state.crm.CRMsList,
        isConnecting: state.crm.isConnecting,
        isTesting: state.crm.isTesting,
        isDisconnecting: state.crm.isDisconnecting,
        isLoading: state.crm.isLoading,
        exportData: state.crm.exportData
    };
}

export default connect(mapStateToProps)(Form.create()(Crm));

