import React from 'react';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import AuroraCardAvatar from 'components/AuroraCardAvatar/AuroraCardAvatar'
import {Typography} from 'antd';

import styles from './Integrations.module.less'
import {getLink, history} from "helpers";
import PropTypes from 'prop-types';

const {Title} = Typography;

class Integrations extends React.Component {

    static contextTypes = {
        router: PropTypes.object
    };

    render() {
        return (
            <NoHeaderPanel>
                <div className={styles.Title}>
                    <Title>All Integrations</Title>
                </div>

                <div className={styles.Body}>
                    <div className={styles.CardFrame}>
                        <AuroraCardAvatar title={'bullhorn'}
                                          onClick={() => history.push(`/dashboard/integrations/1`)}
                                          desc={'bullhorn desc'}
                                          image={getLink('/static/images/CRM/bullhorn.png')}/>
                    </div>

                    <div className={styles.CardFrame}>
                        <AuroraCardAvatar title={'vincere'}
                                          onClick={() => history.push(`/dashboard/integrations/2`)}
                                          desc={'vincere desc'}
                                          image={getLink('/static/images/CRM/vincere.png')}/>
                    </div>

                    <div className={styles.CardFrame}>
                        <AuroraCardAvatar title={'adapt'}
                                          onClick={() => history.push(`/dashboard/integrations/3`)}
                                          desc={'adapt desc'}
                                          image={getLink('/static/images/CRM/adapt.png')}/>
                    </div>
                </div>

            </NoHeaderPanel>
        );
    }
}

export default Integrations;
