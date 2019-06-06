import React from 'react'
import {Icon, Spin, Typography} from 'antd';
import styles from './Marketplace.module.less'
import 'types/CRM_Types';
import {getLink} from "helpers";
import {crmActions} from "store/actions";
import {connect} from 'react-redux';
import AuroraCardAvatar from "components/AuroraCardAvatar/AuroraCardAvatar";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Link} from "react-router-dom";

const {Title, Paragraph, Text} = Typography;

class Marketplace extends React.Component {
    state = {
        /** @type {CRM[]} */
        CRMs: [
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
                title: 'Bullhorn',
                desc: `Bullhorn provides customer relationship management, applicant tracking system and operations software for the staffing industry.`,
                image: getLink('/static/images/CRM/bullhorn.png'),
                type: "Bullhorn",
                status: 'NOT_CONNECTED',
            },
        ]
    };

    componentDidMount() {
        this.props.dispatch(crmActions.getConnectedCRMs())
    }

    componentWillReceiveProps(nextProps) {
        // check the status
        this.setState(
            state => state.CRMs.map(
                crm => {
                    const index = nextProps.CRMsList.findIndex(serverCRM => serverCRM.Type === crm.type);
                    if (index === -1) {
                        // if there is not crm from the server
                        crm.status = 'NOT_CONNECTED';
                        delete crm.ID;
                    } else {
                        // if there is a crm, check if it is failed or connected
                        // and add the ID
                        crm.status = nextProps.CRMsList[index].Status ? "CONNECTED" : "FAILED";
                        crm.ID = nextProps.CRMsList[index].ID
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
                        this.state.CRMs.map((crm, i) =>
                            <div className={styles.CardFrame} key={i}>
                                <Spin spinning={this.props.isLoadingCrms}>
                                    <Link to={{
                                        pathname: `/dashboard/marketplace/${crm.type}`,
                                        state: {crm: crm}
                                    }}>
                                        <AuroraCardAvatar title={crm.title}
                                                          desc={crm.desc}
                                                          image={crm.image}
                                                          status={crm.status}/>
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
        CRMsList: state.crm.CRMsList,
        isLoadingCrms: state.crm.isLoadingCrms
    };
}

export default connect(mapStateToProps)(Marketplace);
