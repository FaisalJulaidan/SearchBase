import React from 'react';

import {Typography} from 'antd';
import styles from "components/ViewBox/ViewBox.module.less";
import PropTypes from 'prop-types';

const {Paragraph} = Typography;

const ViewBox = (props) => {
    return (
        <div className={styles.Box} onClick={() => {
            if (props.onClick) props.onClick()
        }}>
            <div className={styles.Body}>
                <div className={styles.Icon}
                     style={{top: props.iconTop,
                            right: props.iconRight,
                            width: props.iconWidth,
                            height: props.iconHeight
                     }}
                >
                    {props.icon}
                </div>

                {
                    props.icon2 &&
                    <div className={styles.Icon}
                         style={{
                             top: props.iconTop - 10,
                             right: props.iconRight + 170,
                             width: props.iconWidth,
                             height: props.iconHeight
                         }}
                    >
                        {props.icon2}
                    </div>
                }

                <Paragraph level={3} className={styles.Title}>
                    {props.title}
                </Paragraph>

                <Paragraph type="secondary" ellipsis={{rows: 3, expandable: true}} style={{overflowWrap: 'break-word'}}>
                    {props.text}
                </Paragraph>
            </div>


        </div>
    )

};

ViewBox.propTypes = {
    // icon: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    text: PropTypes.string,
};

export default ViewBox
