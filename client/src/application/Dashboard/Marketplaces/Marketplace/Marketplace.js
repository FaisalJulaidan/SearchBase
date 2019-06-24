import React from 'react'
import {Breadcrumb, Form, Modal, Tabs, Typography} from 'antd';
import 'types/Marketplaces_Types';
import {getLink, history} from "helpers";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {marketplacesActions} from "store/actions";
import styles from './Marketplace.module.less'
import {DefaultButton} from './CrmForms/Common'
import {AdaptFeatures, AdaptFormItems, AdaptHeader} from "./CrmForms/Adapt";
import {BullhornFeatures, BullhornFormItems, BullhornHeader} from "./CrmForms/Bullhorn";
import {VincereButtons, VincereFeatures, VincereHeader} from "./CrmForms/Vincere";
import {GreenhouseFeatures, GreenhouseFormItem, GreenhouseHeader} from "./CrmForms/Greenhouse";
import {GoogleButton, GoogleFeatures, GoogleHeader} from './CrmForms/Google'
import {OutlookButton, OutlookFeatures, OutlookHeader} from "./CrmForms/Outlook";
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
            marketplacesActions.connectMarketplace(
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
            marketplacesActions.testMarketplace(
                {
                    type: marketplace.type,
                    auth: {...values}
                }
            )
        );
    });

    disconnectMarketplace = () => this.props.dispatch(marketplacesActions.disconnectMarketplace({ID: this.getMarketplaceObj().ID}));


    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    handleCancel = e => {
        this.setState({
            visible: false,
        });
    };


    /**
     * @param {string} type
     * @param {'header'|'features'|'form'|'button'} place
     * */
    getMarketplaceComponent = (type, place) => {
        const {getFieldDecorator} = this.props.form;
        const layout = {
            labelCol: {span: 6},
            wrapperCol: {span: 14},
        };
        const formOptions = {
            getFieldDecorator,
            layout,
            marketplace: this.getMarketplaceObj(),
            FormItem: FormItem,
            isConnecting: this.props.isConnecting,
            isTesting: this.props.isTesting,
            isDisconnecting: this.props.isDisconnecting,
            openModal: this.showModal,
            disconnectMarketplace: this.disconnectMarketplace,
            connectCRM: this.connectMarketplace,
            testMarketplace: this.testMarketplace,
        };
        const buttonsOptions = {
            disconnectMarketplace: this.disconnectMarketplace,
            isDisconnecting: this.props.isDisconnecting,
            showModal: this.showModal,
            type: this.getMarketplaceObj().type,
            status: this.getMarketplaceObj().status,
            companyID: this.props.companyID
        };

        switch (type) {
            case "Adapt":
                if (place === 'header')
                    return <AdaptHeader/>;
                if (place === 'features')
                    return <AdaptFeatures/>;
                if (place === 'form')
                    return <AdaptFormItems {...formOptions}/>;
                if (place === 'button')
                    return <DefaultButton {...buttonsOptions}/>;
                break;

            case "Bullhorn":
                if (place === 'header')
                    return <BullhornHeader/>;
                if (place === 'features')
                    return <BullhornFeatures/>;
                if (place === 'form')
                    return <BullhornFormItems {...formOptions}/>;
                if (place === 'button')
                    return <DefaultButton {...buttonsOptions}/>;
                break;

            case "Vincere":
                if (place === 'header')
                    return <VincereHeader/>;
                if (place === 'features')
                    return <VincereFeatures/>;
                if (place === 'button')
                    return <VincereButtons {...buttonsOptions}/>;
                break;

            case "Greenhouse":
                if (place === 'header')
                    return <GreenhouseHeader/>;
                if (place === 'features')
                    return <GreenhouseFeatures/>;
                if (place === 'form')
                    return <GreenhouseFormItem {...formOptions}/>;
                if (place === 'button')
                    return <DefaultButton {...buttonsOptions}/>;
                break;

            case "gmail":
                if (place === 'header')
                    return <GoogleHeader/>;
                if (place === 'features')
                    return <GoogleFeatures/>;
                if (place === 'button')
                    return <GoogleButton {...buttonsOptions}/>;
                break;

            case "Outlook":
                if (place === 'header')
                    return <OutlookHeader/>;
                if (place === 'features')
                    return <OutlookFeatures/>;
                if (place === 'button')
                    return <OutlookButton {...buttonsOptions}/>;
                break;
        }
    };

    render() {
        const {title, image, type} = this.getMarketplaceObj();
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
                                <img src={getLink(image)} width={100}
                                     alt={'company logo'}
                                     style={{
                                         float: 'left',
                                         marginRight: 20
                                     }}/>
                                <Title style={{fontSize: '55pt', margin: 0}}>{title}</Title>
                            </div>
                            <div className={styles.Buttons}>
                                {this.getMarketplaceComponent(type, 'button')}
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
