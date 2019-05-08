import React from 'react';
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Typography, Button} from 'antd';

import styles from './CrmView.module.less'
import {getLink, history} from "helpers";
import PropTypes from 'prop-types';

const {Title} = Typography;

class CrmView extends React.Component {
    static contextTypes = {
        router: PropTypes.object
    };

    CRMID = this.props.match.params.id;

    componentDidMount() {
        console.log('I should send request to the server with this id ' + this.CRMID)
    }


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


                </div>

            </NoHeaderPanel>
        );
    }
}

export default CrmView;
