import React from 'react';
import {Tabs, Typography, Spin} from "antd";
import {connect} from 'react-redux';

import './Account.less';
import styles from "./Account.module.less"

import ProfileDetails from "./ProfileDetails/ProfileDetails";
import CompanyDetails from "./CompanyDetails/CompanyDetails";
import Development from './Development/Development'

import {accountActions} from "store/actions/account.actions";
import {developmentActions} from "store/actions/development.actions";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'

const TabPane = Tabs.TabPane;
const {Title, Paragraph} = Typography;


class Account extends React.Component {

    saveProfileDetails = (values) => {
        this.props.dispatch(accountActions.saveProfileDetails(values));
    };

    saveCompanyDetails = (values) => {
        this.props.dispatch(accountActions.saveCompanyDetails(values));
    };

    savePassword = (values) => {
        this.props.dispatch(accountActions.changePassword(values.oldPassword, values.newPassword));
    };

    uploadLogo = async (file) => {
        this.props.dispatch(accountActions.uploadLogo(file));
    };

    deleteLogo = () => this.props.dispatch(accountActions.deleteLogo());


    componentWillMount() {
        this.props.dispatch(accountActions.getAccount());
        this.props.dispatch(developmentActions.fetchDevRequest())
    }

    render() {
        const {account} = this.props;
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <Title className={styles.Title}>
                            Account
                        </Title>
                        <Paragraph type="secondary">
                            Here you can control your profile and company details
                        </Paragraph>
                    </div>

                    <div className={[styles.Body, 'profileTabs'].join(' ')}>
                        {!account ? <Spin/> :

                            <Tabs defaultActiveKey={'1'} size={"large"} animated={false}>
                                <TabPane tab={"Profile"} key={"1"}>
                                    <ProfileDetails account={account}
                                                    saveProfileDetails={this.saveProfileDetails}
                                                    savePassword={this.savePassword}/>
                                </TabPane>

                                <TabPane tab={"Company"} key={"2"}>
                                    <CompanyDetails account={account}
                                                    saveCompanyDetails={this.saveCompanyDetails}
                                                    uploadLogo={this.uploadLogo}
                                                    deleteLogo={this.deleteLogo}/>
                                </TabPane>
                                <TabPane tab={"Development"} key={"3"}>
                                    <Development webhooks={this.props.webhooks}/>
                                </TabPane>
                            </Tabs>
                        }
                    </div>
                </NoHeaderPanel>
            </>
        );
    }
}

function mapStateToProps(state) {
    console.log(state)
    return {
        account: state.account.account,
        webhooks: state.development.webhooks
    };
}

export default connect(mapStateToProps)(Account);
