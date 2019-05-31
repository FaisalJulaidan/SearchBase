import React from 'react'
import {Icon, Spin, Typography} from 'antd';
import styles from './Crms.module.less'
import 'types/CRM_Types';
import {getLink} from "helpers";
import {crmActions} from "store/actions";
import {connect} from 'react-redux';
import AuroraCardAvatar from "components/AuroraCardAvatar/AuroraCardAvatar";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Link} from "react-router-dom";

const {Title, Paragraph, Text} = Typography;

class Crms extends React.Component {
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
                desc: `Bond Adapt, specialist portfolio of recruitment software applications has earned a reputation for increasing business growth.`,
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
                <div className={styles.Title}>
                    <div className={styles.Details}>
                        <Title> <Icon type="interation"/> CRMs List</Title>
                        <Paragraph type="secondary">
                            <Text>Desc</Text>
                        </Paragraph>
                    </div>
                </div>

                <div className={styles.Body}>
                    {
                        this.state.CRMs.map((crm, i) =>
                            <div className={styles.CardFrame} key={i}>
                                <Spin spinning={this.props.isLoading}>
                                    <Link to={{
                                        pathname: `/dashboard/crmlist/${crm.type}`,
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
        isLoading: state.crm.isLoading
    };
}

export default connect(mapStateToProps)(Crms);
