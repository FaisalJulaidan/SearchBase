import React from 'react';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import AuroraCardAvatar from 'components/AuroraCardAvatar/AuroraCardAvatar'
import {Typography, Button} from 'antd';

import styles from './Integrations.module.less'
import {getLink} from "helpers";
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
                    <Button onClick={this.context.router?.history?.goBack}
                            className={styles.BackButton}
                            type="primary" icon="left" shape="circle"/>
                    <Title>All Integrations</Title>
                </div>

                <div className={styles.Body}>
                    <div className={styles.CardFrame}>
                        <AuroraCardAvatar title={'bullhorn'}
                                          desc={'bullhorn desc'}
                                          image={getLink('/static/images/CRM/bullhorn.png')}/>
                    </div>

                    <div className={styles.CardFrame}>
                        <AuroraCardAvatar title={'vincere'}
                                          desc={'vincere desc'}
                                          image={getLink('/static/images/CRM/vincere.png')}/>
                    </div>

                    <div className={styles.CardFrame}>
                        <AuroraCardAvatar title={'adapt'}
                                          desc={'adapt desc'}
                                          image={getLink('/static/images/CRM/adapt.png')}/>
                    </div>

                </div>

            </NoHeaderPanel>
        );
    }
}

export default Integrations;
