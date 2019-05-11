import React from 'react';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import AuroraCardAvatar from 'components/AuroraCardAvatar/AuroraCardAvatar'
import {Typography, Spin} from 'antd';
import {connect} from 'react-redux';
import styles from './Integrations.module.less'
import {getLink, history} from "helpers";
import PropTypes from 'prop-types';
import shortid from 'shortid';
import {integrationsActions} from "store/actions";
const {Title} = Typography;


/**
 * Date type
 @typedef CRM
 @type {Object}
 @property {string} title
 @property {string} desc
 @property {function} link
 @property {string} image
 @property {('CONNECTED'|'NOT_CONNECTED'|'FAILED')} status
 */


class Integrations extends React.Component {

    static contextTypes = {
        router: PropTypes.object
    };

    state = {
        /** @type {CRM[]} */
        CRMs: [
            {
                title: 'Bullhorn',
                desc: 'Bullhorn Desc',
                link: () => history.push(`/dashboard/integrations/2`),
                image: getLink('/static/images/CRM/bullhorn.png'),
                type: "Bullhorn",
                status: 'NOT_CONNECTED'
            },
            {
                title: 'Vincere',
                desc: 'Vincere Desc',
                link: () => history.push(`/dashboard/integrations/3`),
                image: getLink('/static/images/CRM/vincere.png'),
                type: "Vincere",
                status: 'FAILED'
            },
            {
                title: 'Adapt',
                desc: 'Adapt Desc',
                link: () => history.push(`/dashboard/integrations/1`),
                image: getLink('/static/images/CRM/adapt.png'),
                type: "Adapt",
                status: 'NOT_CONNECTED'
            }
        ],
        isLoading: true
    };

    componentDidMount() {
        this.props.dispatch(integrationsActions.getConnectedCRMs())
    }

    componentWillReceiveProps(nextProps) {
        nextProps.CRMsList
            .forEach(serverCRM => {
                /** @type {CRM} */
                let currentCRM = this.state.CRMs.find(crm => crm.type === serverCRM.Type);

                if (currentCRM.status)
                    currentCRM.status = "CONNECTED";
                else
                    currentCRM.status = "FAILED";

                this.setState({
                    CRMs: [...this.state.CRMs],
                    isLoading: false
                })
            });
    }

    render() {
        const {CRMs} = this.state;
        return (
            <Spin spinning={this.state.isLoading}>
                <NoHeaderPanel>
                    <div className={styles.Title}>
                        <Title>All Integrations</Title>
                    </div>

                    <div className={styles.Body}>
                        {
                            CRMs.map(CRM =>
                                <div className={styles.CardFrame}
                                     key={shortid.generate()}>
                                    <AuroraCardAvatar title={CRM.title}
                                                      onClick={CRM.link}
                                                      desc={CRM.desc}
                                                      image={CRM.image}
                                                      status={CRM.status}
                                    />
                                </div>
                            )
                        }
                    </div>
                </NoHeaderPanel>
            </Spin>
        );
    }
}

function mapStateToProps(state) {
    return {
        CRMsList: state.integrations.CRMsList,
    };
}

export default connect(mapStateToProps)(Integrations);
