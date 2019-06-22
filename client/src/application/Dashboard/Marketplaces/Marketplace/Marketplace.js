import React from 'react'
import {Icon, Spin, Typography} from 'antd';
import styles from './Marketplace.module.less'
import 'types/Marketplaces_Types';
import {getLink} from "helpers";
import {marketplacesActions} from "store/actions";
import {connect} from 'react-redux';
import AuroraCardAvatar from "components/AuroraCardAvatar/AuroraCardAvatar";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Link} from "react-router-dom";

import axios from 'axios'

const {Title, Paragraph, Text} = Typography;

class Marketplace extends React.Component {
    state = {
    };

    componentDidMount() {

    }


    render() {
        return (
            <NoHeaderPanel>
                <div className={styles.Header}>
                    hi
                </div>

                <div className={styles.Body}>
                    hi
                </div>
            </NoHeaderPanel>
        )
    }
}


export default Marketplace;
