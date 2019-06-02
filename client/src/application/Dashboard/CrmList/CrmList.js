import React from 'react';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import AuroraCardAvatar from 'components/AuroraCardAvatar/AuroraCardAvatar'
import {Spin, Typography,Icon} from 'antd';
import {connect} from 'react-redux';
import styles from './CrmList.module.less'
import {deepClone, getLink, history} from "helpers";
import PropTypes from 'prop-types';
import shortid from 'shortid';
import {crmActions} from "store/actions";
import 'types/CRM_Types';

const {Title, Paragraph, Text} = Typography;


class CrmList extends React.Component {

    static contextTypes = {
        router: PropTypes.object
    };

    state = {
        /** @type {CRM[]} */
        CRMs: [
            {
                title: 'Adapt',
                desc: `Bond Adapt, specialist portfolio of recruitment software applications has earned a reputation for increasing business growth.`,
                link: () => history.push({
                    pathname: `/dashboard/crmlist/adapt`,
                    state: {CRMs: this.state.CRMs}
                }),
                image: getLink('/static/images/CRM/adapt.png'),
                type: "Adapt",
                status: 'NOT_CONNECTED',
            },
            {
                title: 'Bullhorn',
                desc: 'Bullhorn Desc',
                link: () => history.push(`/dashboard/crmlist/bullhorn`),
                image: getLink('/static/images/CRM/bullhorn.png'),
                type: "Bullhorn",
                status: 'NOT_CONNECTED',
            },
            // {
            //     title: 'Vincere',
            //     desc: 'Vincere Desc',
            //     link: () => history.push({
            //         pathname: `/dashboard/crmlist/vincere`,
            //         state: {CRMs: this.state.CRMs}
            //     }),
            //     image: getLink('/static/images/CRM/vincere.png'),
            //     type: "Vincere",
            //     status: 'NOT_CONNECTED',
            // },
            // {
            //     title: 'Greenhouse',
            //     desc: 'Greenhouse Desc',
            //     link: () => history.push({
            //         pathname: `/dashboard/crmlist/adapt`,
            //         state: {CRMs: this.state.CRMs}
            //     }),
            //     image: 'https://jumpcloud.com/wp-content/uploads/2017/12/jc-sso-greenhouseio.png',
            //     type: "Adapt",
            //     status: 'NOT_CONNECTED',
            // },
            // {
            //     title: 'Mercury Xrm',
            //     desc: 'Mercury Xrm Desc',
            //     link: () => history.push({
            //         pathname: `/dashboard/crmlist/adapt`,
            //         state: {CRMs: this.state.CRMs}
            //     }),
            //     image: 'https://www.mercuryxrm.co.uk/wp-content/uploads/2015/07/Mercury-Logo-Jan-2015_With-Strapline-e1436358412150.jpg',
            //     type: "Adapt",
            //     status: 'NOT_CONNECTED',
            // },
            // {
            //     title: 'Access Group',
            //     desc: 'Access Group Desc',
            //     link: () => history.push({
            //         pathname: `/dashboard/crmlist/adapt`,
            //         state: {CRMs: this.state.CRMs}
            //     }),
            //     image: 'https://www.theaccessgroup.com/media/17970/accessgroup.png',
            //     type: "Adapt",
            //     status: 'NOT_CONNECTED',
            // }
        ],
        isLoading: true
    };


    componentDidMount() {
        this.props.dispatch(crmActions.getConnectedCRMs())
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.CRMsList[0])
            nextProps.CRMsList
                .forEach(serverCRM => {
                    /** @type {CRM} */
                    let currentCRM = this.state.CRMs.find(crm => crm.type === serverCRM.Type);
                    currentCRM.ID = serverCRM.ID;
                    currentCRM.status = serverCRM.Status ? "CONNECTED" : "FAILED";

                    this.setState({
                        CRMs: [...this.state.CRMs],
                        isLoading: false
                    })
                });
        else
            this.setState({isLoading: false})
    }

    render() {
        const {CRMs} = this.state;
        return (
            <NoHeaderPanel>
                <div className={styles.Title}>
                    <div className={styles.Details}>
                        <Title> <Icon type="interation"/> CRMs List</Title>
                        <Paragraph type="secondary">
                            From the list below, choose your CRM or ATS for your account to be directly connected.
                            If you need help with the setup or wish to contact us to arrange an integration with your
                            provider,
                            please contact us at:
                            <Text code><a target={'_blank'}
                                          href={"mailto:info@thesearchbase.com"}>
                                info@thesearchbase.com
                            </a></Text>.
                        </Paragraph>
                    </div>

                </div>

                <div className={styles.Body}>
                    {
                        CRMs.map(/**CRM*/CRM =>
                            <div className={styles.CardFrame} key={shortid.generate()}>
                                <Spin spinning={this.state.isLoading}>
                                    <AuroraCardAvatar title={CRM.title}
                                                      onClick={() => history.push(`/dashboard/crmlist/${CRM.type}`, {CRM: deepClone(CRM)})}
                                                      desc={CRM.desc}
                                                      image={CRM.image}
                                                      status={CRM.status}
                                    />
                                </Spin>
                            </div>
                        )
                    }
                </div>
            </NoHeaderPanel>
        );
    }
}

function mapStateToProps(state) {
    return {
        CRMsList: state.crm.CRMsList,
    };
}

export default connect(mapStateToProps)(CrmList);
