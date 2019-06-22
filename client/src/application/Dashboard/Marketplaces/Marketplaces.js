import React from 'react'
import {Icon, Spin, Typography} from 'antd';
import styles from './Marketplaces.module.less'
import 'types/Marketplaces_Types';
import {getLink} from "helpers";
import {marketplacesActions} from "store/actions";
import {connect} from 'react-redux';
import AuroraCardAvatar from "components/AuroraCardAvatar/AuroraCardAvatar";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Link} from "react-router-dom";

import axios from 'axios'

const {Title, Paragraph, Text} = Typography;

class Marketplaces extends React.Component {
    state = {
        /** @type {Marketplace[]} */
        marketplaces: [
            {
                title: 'Adapt',
                desc: `Bond Adapt, specialist portfolio of recruitment software applications has earned a reputation for increasing business growth.`,
                image: getLink('/static/images/CRM/adapt.png'),
                type: "Adapt",
                status: 'NOT_CONNECTED',
            },
            {
                title: 'Bullhorn',
                desc: `Bullhorn provides customer relationship management, applicant tracking system and operations software for the staffing industry.`,
                image: getLink('/static/images/CRM/bullhorn.png'),
                type: "Bullhorn",
                status: 'NOT_CONNECTED',
            },
            {
                title: 'Vincere',
                desc: `Vincere provides customer relationship management, applicant tracking system and operations software for the staffing industry.`,
                image: getLink('/static/images/CRM/vincere.png'),
                type: "Vincere",
                status: 'NOT_CONNECTED',
            },
            {
                title: 'Greenhouse',
                desc: `Greenhouse works seamlessly with over 220 partners and third-party apps and technologies, enabling you to solve specific problems.`,
                image: getLink('/static/images/CRM/greenhouse.png'),
                type: "Greenhouse",
                status: 'NOT_CONNECTED',
            },
            {
                title: 'Outlook Calendar',
                desc: `Calendar is the calendar and scheduling component of Outlook that is fully integrated with email, contacts, and other features.`,
                image: getLink('/static/images/CRM/outlook-calendar.png'),
                type: "Outlook",
                status: 'NOT_CONNECTED'
            },
            {
                title: 'Google Calendar',
                desc: `Google Calendar is a time-management and scheduling calendar service lets you keep track of important events, share your schedule.`,
                image: getLink('/static/images/CRM/gmail.jpg'),
                type: "gmail",
                status: 'NOT_CONNECTED'
            },
        ]
    };

    componentDidMount() {
        let loc = this.props.location.search.replace("?", "").split("&");
        let isGoogleAuthorize = loc.filter(e => e.substring(0, "googleVerification".length) === "googleVerification").length > 0;
        if (isGoogleAuthorize) {
            let code = loc.filter(e => e.substr(0, 4) === "code")[0].replace("code=", "");
            axios.post("/api/calendar/google/authorize", {code})
        }
        this.props.dispatch(marketplacesActions.getConnectedCRMs())
    }

    componentWillReceiveProps(nextProps) {
        // check the status
        this.setState(
            state => state.marketplaces.map(
                marketplaces => {
                    const index = nextProps.marketplacesList.findIndex(serverCRM => serverCRM.Type === marketplaces.type);

                    if (marketplaces.status === 'Comming Soon')
                        return 0;

                    if (index === -1) {
                        // if there is not marketplace from the server
                        marketplaces.status = 'NOT_CONNECTED';
                        delete marketplaces.ID;
                    } else {
                        // if there is a marketplace, check if it is failed or connected
                        // and add the ID
                        marketplaces.status = nextProps.marketplacesList[index].Status ? "CONNECTED" : "FAILED";
                        marketplaces.ID = nextProps.marketplacesList[index].ID;
                    }
                }
            )
        )
    }

    render() {
        return (
            <NoHeaderPanel>
                <div className={styles.Header}>
                    <Title className={styles.Title}>
                        <Icon type="interation"/> Marketplace
                    </Title>
                    <Paragraph type="secondary">
                        From the list below, choose your CRM or ATS for your account to be directly connected.
                        If you need help with the setup or wish to contact us to arrange an integration with
                        your provider, please contact us at:
                        <Text code>
                            <a target={'_blank'} href={"mailto:info@thesearchbase.com"} style={{cursor: 'pointer'}}>
                                info@thesearchbase.com
                            </a>
                        </Text>.
                    </Paragraph>
                </div>

                <div className={styles.Body}>
                    {
                        this.state.marketplaces.map((marketplace, i) =>
                            <div className={styles.CardFrame} key={i}>
                                <Spin spinning={this.props.isLoadingMarketplaces}>
                                    <Link to={{
                                        pathname: `/dashboard/marketplaces/${marketplace.type}`,
                                        state: {marketplace: marketplace, companyID: this.props.companyID}
                                    }}>
                                        <AuroraCardAvatar title={marketplace.title}
                                                          desc={marketplace.desc}
                                                          image={marketplace.image}
                                                          status={marketplace.status}
                                                          disabled={marketplace.disabled}
                                        />
                                    </Link>
                                </Spin>
                            </div>
                        )
                    }
                </div>
            </NoHeaderPanel>
        )
    }
}


function mapStateToProps(state) {
    return {
        marketplacesList: state.marketplace.marketplacesList,
        companyID: state.marketplace.companyID,
        isLoadingMarketplaces: state.marketplace.isLoadingMarketplaces
    };
}

export default connect(mapStateToProps)(Marketplaces);
