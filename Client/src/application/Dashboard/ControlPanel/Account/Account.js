import React from 'react';
import {Tabs, Typography, Spin} from "antd";
import {connect} from 'react-redux';
import queryString from 'query-string';

import './Account.less';
import styles from "./Account.module.less"

import ProfileDetails from "./ProfileDetails/ProfileDetails";
import CompanyDetails from "./CompanyDetails/CompanyDetails";
import Development from './Development/Development'

import {accountActions} from "store/actions/account.actions";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'

const TabPane = Tabs.TabPane;
const {Title, Paragraph} = Typography;


class Account extends React.Component {

    state = {
        key: null,
        defaultTab: 'Conversations'
    };

    componentWillMount() {
        this.props.dispatch(accountActions.getAccount());
        // Set tab from url search params
        let params = queryString.parse(this.props.location.search);
        if (['Profile', 'Company', 'Development'].includes(params['tab']))
            this.setState({ defaultTab: params['tab'] });
    }

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

                            <Tabs onChange={key => this.setState({ key: key })} defaultActiveKey={this.state.defaultTab} size={"large"} animated={false}>
                                <TabPane tab={"Profile"} key={"Profile"}>
                                    <ProfileDetails account={account}
                                                    saveProfileDetails={this.saveProfileDetails}
                                                    savePassword={this.savePassword}/>
                                </TabPane>

                                <TabPane tab={"Company"} key={"Company"}>
                                    <CompanyDetails account={account}
                                                    saveCompanyDetails={this.saveCompanyDetails}
                                                    uploadLogo={this.uploadLogo}
                                                    deleteLogo={this.deleteLogo}/>
                                </TabPane>
                                <TabPane tab={"Development"} key={"Development"}>
                                    <Development/>
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
    return {
        account: state.account.account,
    };
}

export default connect(mapStateToProps)(Account);
