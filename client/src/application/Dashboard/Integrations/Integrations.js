import React from 'react';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import AuroraCardAvatar from 'components/AuroraCardAvatar/AuroraCardAvatar'
import {Typography, Spin} from 'antd';
import {connect} from 'react-redux';
import styles from './Integrations.module.less'
import {getLink, history, deepClone} from "helpers";
import PropTypes from 'prop-types';
import shortid from 'shortid';
import {integrationsActions} from "store/actions";
import 'types/CRM_Types';

const {Title, Paragraph, Text} = Typography;


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
                link: () => history.push(`/dashboard/integrations/bullhorn`),
                image: getLink('/static/images/CRM/bullhorn.png'),
                type: "Bullhorn",
                status: 'NOT_CONNECTED',
            },
            {
                title: 'Vincere',
                desc: 'Vincere Desc',
                link: () => history.push({
                    pathname: `/dashboard/integrations/vincere`,
                    state: {CRMs: this.state.CRMs}
                }),
                image: getLink('/static/images/CRM/vincere.png'),
                type: "Vincere",
                status: 'NOT_CONNECTED',
            },
            {
                title: 'Adapt',
                desc: 'Adapt Desc',
                link: () => history.push({
                    pathname: `/dashboard/integrations/adapt`,
                    state: {CRMs: this.state.CRMs}
                }),
                image: getLink('/static/images/CRM/adapt.png'),
                type: "Adapt",
                status: 'NOT_CONNECTED',
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
            <NoHeaderPanel>
                <div className={styles.Title}>
                    <div className={styles.Details}>
                        <Title>All Integrations</Title>
                        <Paragraph type="secondary">
                            We supply a series of design principles, practical patterns and high quality design
                            resources
                            (<Text code>Sketch</Text> and <Text code>Axure</Text>), to help people create their
                            product
                            prototypes beautifully and efficiently.
                        </Paragraph>
                    </div>

                </div>

                <div className={styles.Body}>
                    {
                        CRMs.map(/**CRM*/CRM =>
                            <div className={styles.CardFrame} key={shortid.generate()}>
                                <Spin spinning={this.state.isLoading}>
                                    <AuroraCardAvatar title={CRM.title}
                                                      onClick={() => history.push(`/dashboard/integrations/${CRM.type}`, {CRM: deepClone(CRM)})}
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
        CRMsList: state.integrations.CRMsList,
    };
}

export default connect(mapStateToProps)(Integrations);
