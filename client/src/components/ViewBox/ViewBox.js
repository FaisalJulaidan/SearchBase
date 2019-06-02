import React from 'react';

import {Typography} from 'antd';
import styles from "components/ViewBox/ViewBox.module.less";
import PropTypes from 'prop-types';
import {AutoPilotIcon} from 'components/SVGs'

const {Paragraph} = Typography;

const ViewBox = (props) => {
    return (
        <div className={styles.Box}>
            <div className={styles.Body}>
                <div className={styles.Icon}>
                    {props.icon}
                </div>

                <Paragraph level={3} className={styles.Title}>
                    {props.title}
                </Paragraph>

                <Paragraph type="secondary" ellipsis={{rows: 2, expandable: true}} style={{overflowWrap: 'break-word'}}>
                    {props.text}
                </Paragraph>
            </div>


        </div>
    )

};

ViewBox.propTypes = {
    icon: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
};

export default ViewBox
