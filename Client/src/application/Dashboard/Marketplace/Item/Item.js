import React from 'react'
import {Breadcrumb, Form, Modal, Tabs, Typography} from 'antd';
import 'types/Marketplace_Types';
import {getLink, history} from "helpers";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {marketplaceActions} from "store/actions";
import styles from './Item.module.less'
import {DefaultButton} from './Components/Common'
import {AdaptFeatures, AdaptFormItems, AdaptHeader} from "./Components/Adapt";
import {BullhornFeatures, BullhornHeader} from "./Components/Bullhorn";
import {VincereFeatures, VincereHeader} from "./Components/Vincere";
import {GreenhouseFeatures, GreenhouseFormItem, GreenhouseHeader} from "./Components/Greenhouse";
import {GoogleFeatures, GoogleHeader} from './Components/Google'
import {OutlookFeatures, OutlookHeader} from "./Components/Outlook";
import data from '../Items.json'
import {connect} from 'react-redux';

const TabPane = Tabs.TabPane;
const FormItem = Form.Item;
const {Title, Paragraph, Text} = Typography;

class Item extends React.Component {

    state = {visible: false};

    /**@type {MarketplaceItem}*/
    marketplaceItem = data.Items.find(/**@type {MarketplaceItem}*/item => item.type === this.props.match.params.type);

    componentWillMount() {
        // this.props.dispatch(marketplaceActions.exportRecruiterValueReport({Name: marketplace.type}))
        this.props.dispatch(marketplaceActions.pingMarketplace(this.marketplaceItem.type))
    }

    componentWillReceiveProps(nextProps) {
        this.marketplaceItem.status = nextProps.connectionStatus;
        // if (nextProps.exportData) {
        //     marketplace.exportData = nextProps.exportData;
        // }
    }

    connectMarketplace = () => this.props.form.validateFields((err, values) => {
        if (err) return;
        this.props.dispatch(marketplaceActions.connectMarketplace(this.marketplaceItem.type, {...values}))
    });

    disconnectMarketplace = () => this.props.dispatch(marketplaceActions.disconnectMarketplace(this.marketplaceItem.type));

    showModal = () => this.setState({visible: true});

    handleCancel = () => this.setState({visible: false});


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
            marketplace: this.marketplaceItem,
            FormItem: FormItem,
            isConnecting: this.props.isConnecting,
            isDisconnecting: this.props.isDisconnecting,
            openModal: this.showModal,
            disconnectMarketplace: this.disconnectMarketplace,
            connectMarketplace: this.connectMarketplace,
        };
        const buttonsOptions = {
            disconnectMarketplace: this.disconnectMarketplace,
            isDisconnecting: this.props.isDisconnecting,
            showModal: this.showModal,
            type: this.marketplaceItem.type,
            status: this.marketplaceItem.status,
            isConnecting: this.props.isPinging
        };

        const windowObject = {
            url: '',
            target: 'Ratting',
            features: 'width=600,height=600,0,top=40%,right=30%,status=0',
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
                    return <DefaultButton buttonText={'Connect to Adapt'} {...buttonsOptions}/>;
                break;

            case "Bullhorn":
                if (place === 'header')
                    return <BullhornHeader/>;
                if (place === 'features')
                    return <BullhornFeatures/>;
                if (place === 'button') {
                    windowObject.url = "https://auth.bullhornstaffing.com/oauth/authorize?response_type=code&redirect_uri=https://www.thesearchbase.com/api/bullhorn_callback&client_id=7719607b-7fe7-4715-b723-809cc57e2714";
                    return <DefaultButton buttonText={'Connect to Bullhorn'}
                                          windowObject={windowObject}
                                          {...buttonsOptions}/>;
                }
                break;

            case "Vincere":
                if (place === 'header')
                    return <VincereHeader/>;
                if (place === 'features')
                    return <VincereFeatures/>;
                if (place === 'button') {
                    windowObject.url = "https://id.vincere.io/oauth2/authorize?client_id=9829f4ad-3ff3-4d00-8ecf-e5d7fa2983d1&response_type=code&redirect_uri=https://www.thesearchbase.com/api/marketplace_callback";
                    return <DefaultButton buttonText={'Connect to Vincere'}
                                          windowObject={windowObject}
                                          {...buttonsOptions}/>;
                }
                break;

            case "Greenhouse":
                if (place === 'header')
                    return <GreenhouseHeader/>;
                if (place === 'features')
                    return <GreenhouseFeatures/>;
                if (place === 'form')
                    return <GreenhouseFormItem {...formOptions}/>;
                if (place === 'button')
                    return <DefaultButton buttonText={'Connect to Greenhouse'} {...buttonsOptions}/>;
                break;

            case "Google":
                if (place === 'header')
                    return <GoogleHeader/>;
                if (place === 'features')
                    return <GoogleFeatures/>;
                if (place === 'button') {
                    const clientID = "623652835897-tj9rf1v6hd1tak5bv5hr4bq9hrvjns95.apps.googleusercontent.com";
                    const responseType = "code";
                    const scope = "https://www.googleapis.com/auth/calendar";
                    const redirectURI = getLink("/dashboard/marketplace?googleVerification=true");

                    windowObject.url = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientID}&response_type=${responseType}&scope=${scope}&redirect_uri=${redirectURI}&access_type=offline`;
                    return <DefaultButton buttonText={'Connect to Google'}
                                          windowObject={windowObject}
                                          {...buttonsOptions}/>;
                }
                break;

            case "Outlook":
                if (place === 'header')
                    return <OutlookHeader/>;
                if (place === 'features')
                    return <OutlookFeatures/>;
                if (place === 'button') {
                    windowObject.url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=0978960c-c837-479f-97ef-a75be4bbacd4&redirect_uri=https://www.thesearchbase.com/api/marketplace_callback&response_mode=query&scope=openid+https%3A%2F%2Fgraph.microsoft.com%2Fcalendars.readwrite%20+offline_access";
                    return <DefaultButton buttonText={'Connect to Outlook'}
                                          windowObject={windowObject}
                                          {...buttonsOptions}/>;
                }
                break;
        }
    };

    render() {
        const {title, image, type} = this.marketplaceItem;
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <div style={{marginBottom: 20}}>
                            <Breadcrumb>
                                <Breadcrumb.Item>
                                    <a href={"javascript:void(0);"}
                                       onClick={() => history.push('/dashboard/marketplace')}>
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
                                <Title style={{fontSize: '38pt', margin: "15px 0 0 0"}}>{title}</Title>
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
                        <Tabs defaultActiveKey="1" size={'large'}>
                            <TabPane tab="Feature" key="1">
                                {this.getMarketplaceComponent(type, 'features')}
                            </TabPane>
                        </Tabs>
                    </div>
                </NoHeaderPanel>
                <Modal
                    title="Connection Modal"
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
        connectionStatus: state.marketplace.connectionStatus,
        isPinging: state.marketplace.isPinging,
        isDisconnecting: state.marketplace.isDisconnecting,

        companyID: state.marketplace.companyID,
        isConnecting: state.marketplace.isConnecting,
        isLoading: state.marketplace.isLoading,
        exportData: state.marketplace.exportData,
    };
}

export default connect(mapStateToProps)(Form.create()(Item));