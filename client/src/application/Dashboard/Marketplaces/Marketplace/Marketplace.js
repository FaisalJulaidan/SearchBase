import React from 'react'
import {Breadcrumb, Button, Form, Modal, Popconfirm, Tabs, Typography} from 'antd';
import 'types/Marketplaces_Types';
import {history} from "helpers";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {marketplacesActions} from "store/actions";
import styles from './Marketplace.module.less'
import {AdaptFeatures, AdaptFormItems, AdaptHeader} from "./CrmForms/Adapt";
import {BullhornFeatures, BullhornFormItems, BullhornHeader} from "./CrmForms/Bullhorn";
import {VincereFeatures, VincereFormItems, VincereHeader} from "./CrmForms/Vincere";
import {GreenhouseFeatures, GreenhouseFormItem, GreenhouseHeader} from "./CrmForms/Greenhouse";
import {GoogleFeatures, GoogleFormItems, GoogleHeader} from './CrmForms/Google'
import {OutlookFeatures, OutlookFormItems, OutlookHeader} from "./CrmForms/Outlook";
import data from '../Marketplaces.json'
import {connect} from 'react-redux';

const TabPane = Tabs.TabPane;
const FormItem = Form.Item;
const {Title, Paragraph, Text} = Typography;

class Marketplace extends React.Component {

    state = {visible: false};

    /**@return {Marketplace}*/
    getMarketplaceObj = () => data.Marketplaces.find(marketplace => marketplace.type === this.props.match.params.type);


    componentWillMount() {
        const marketplace = this.getMarketplaceObj();
        this.props.dispatch(marketplacesActions.exportRecruiterValueReport({Name: marketplace.type}))
    }

    componentWillReceiveProps(nextProps) {
        const marketplace = this.getMarketplaceObj();
        const index = nextProps.marketplacesList.findIndex(serverCRM => serverCRM.Type === marketplace.type);
        if (index === -1) {
            // if there is not marketplace from the server
            marketplace.status = 'NOT_CONNECTED';
            marketplace.companyID = nextProps.companyID;
            delete marketplace.ID;
        } else {
            // if there is a marketplace, check if it is failed or connected
            // and add the ID
            marketplace.status = nextProps.marketplacesList[index].Status ? "CONNECTED" : "FAILED";
            marketplace.ID = nextProps.marketplacesList[index].ID;
        }
        if (nextProps.exportData) {
            marketplace.exportData = nextProps.exportData;
        }
    }

    connectMarketplace = () => this.props.form.validateFields((err, values) => {
        if (err) return;
        const marketplace = this.getMarketplaceObj();
        this.props.dispatch(
            marketplacesActions.connectCrm(
                {
                    type: marketplace.type,
                    auth: {...values}
                }
            )
        );
    });

    testMarketplace = () => this.props.form.validateFields((err, values) => {
        if (err) return;
        const marketplace = this.getMarketplaceObj();
        this.props.dispatch(
            marketplacesActions.testCrm(
                {
                    type: marketplace.type,
                    auth: {...values}
                }
            )
        );
    });

    disconnectMarketplace = () => this.props.dispatch(marketplacesActions.disconnectCrm({ID: this.getMarketplaceObj().ID}));


    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    handleOk = e => {
        this.setState({
            visible: false,
        });
    };

    handleCancel = e => {
        this.setState({
            visible: false,
        });
    };


    /**
     * @param {string} type
     * @param {'header'|'features'|'form'|'buttons'} place
     * */
    getMarketplaceComponent = (type, place) => {
        const {getFieldDecorator} = this.props.form;
        const layout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const options = {
            getFieldDecorator,
            layout,
            marketplace: this.getMarketplaceObj(),
            FormItem: FormItem,
            isConnecting: this.props.isConnecting,
            isTesting: this.props.isTesting,
            isDisconnecting: this.props.isDisconnecting,
            openModal: this.showModal,
            disconnectCRM: this.disconnectMarketplace,
            connectCRM: this.connectMarketplace,
            testCRM: this.testMarketplace,
        };
        switch (type) {
            case "Adapt":
                if (place === 'header')
                    return <AdaptHeader/>;
                if (place === 'features')
                    return <AdaptFeatures/>;
                if (place === 'form')
                    return <AdaptFormItems {...options}/>;
                break;

            case "Bullhorn":
                if (place === 'header')
                    return <BullhornHeader/>;
                if (place === 'features')
                    return <BullhornFeatures/>;
                if (place === 'form')
                    return <BullhornFormItems {...options}/>;
                break;

            case "Vincere":
                if (place === 'header')
                    return <VincereHeader/>;
                if (place === 'features')
                    return <VincereFeatures/>;
                if (place === 'form')
                    return <VincereFormItems {...options}/>;
                break;

            case "Greenhouse":
                if (place === 'header')
                    return <GreenhouseHeader/>;
                if (place === 'features')
                    return <GreenhouseFeatures/>;
                if (place === 'form')
                    return <GreenhouseFormItem {...options}/>;
                break;

            case "gmail":
                if (place === 'header')
                    return <GoogleHeader/>;
                if (place === 'features')
                    return <GoogleFeatures/>;
                if (place === 'form')
                    return <GoogleFormItems {...options}/>;
                break;

            case "Outlook":
                if (place === 'header')
                    return <OutlookHeader/>;
                if (place === 'features')
                    return <OutlookFeatures/>;
                if (place === 'form')
                    return <OutlookFormItems {...options}/>;
                break;
        }
    };

    render() {
        const type = this.getMarketplaceObj().type;
        const status = this.getMarketplaceObj().status;
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <div style={{marginBottom: 20}}>
                            <Breadcrumb>
                                <Breadcrumb.Item>
                                    <a href={"javascript:void(0);"}
                                       onClick={() => history.push('/dashboard/marketplaces')}>
                                        Marketplace
                                    </a>
                                </Breadcrumb.Item>
                                <Breadcrumb.Item>{type}</Breadcrumb.Item>
                            </Breadcrumb>
                        </div>

                        <div className={styles.HeadBar}>
                            <div className={styles.Title}>
                                <Title level={2}>{type}</Title>
                            </div>
                            <div className={styles.Buttons}>

                                {
                                    (status === "CONNECTED" || status === "FAILED")
                                    &&
                                    <Popconfirm
                                        placement={'bottomRight'}
                                        title="Chatbot conversations will no longer be synced with Adapt account"
                                        onConfirm={this.disconnectMarketplace}
                                        okType={'danger'}
                                        okText="Disconnect"
                                        cancelText="No"
                                    >
                                        <Button type="danger" disabled={this.props.isDisconnecting}>Disconnect</Button>
                                    </Popconfirm>
                                }

                                {
                                    status === "NOT_CONNECTED" &&
                                    <Button type="primary" onClick={this.showModal}>Connect</Button>
                                }
                            </div>
                        </div>

                        <div className={styles.Desc}>
                            {this.getMarketplaceComponent(type, 'header')}
                        </div>

                    </div>

                    <div className={styles.Body}>
                        <Tabs defaultActiveKey="1">
                            <TabPane tab="Feature" key="1">
                                {this.getMarketplaceComponent(type, 'features')}
                            </TabPane>
                        </Tabs>
                    </div>
                </NoHeaderPanel>
                <Modal
                    title="Basic Modal"
                    visible={this.state.visible}
                    onCancel={this.handleCancel}
                    footer={null}>
                    <Form layout='horizontal'>
                        {this.getMarketplaceComponent(type, 'form')}
                    </Form>
                </Modal>
            </>
        )
    }
}


function mapStateToProps(state) {
    return {
        marketplacesList: state.marketplace.marketplacesList,
        companyID: state.marketplace.companyID,
        isConnecting: state.marketplace.isConnecting,
        isTesting: state.marketplace.isTesting,
        isDisconnecting: state.marketplace.isDisconnecting,
        isLoading: state.marketplace.isLoading,
        exportData: state.marketplace.exportData,
    };
}

export default connect(mapStateToProps)(Form.create()(Marketplace));
