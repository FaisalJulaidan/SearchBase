import React from 'react';

import {Typography, Dropdown, Menu} from 'antd';
import styles from "components/ViewBox/ViewBox.module.less";
import PropTypes from 'prop-types';

const {Paragraph} = Typography;



const ViewBox = (props) => {

    let optionsMenu = null;
    if(props.optionsMenuItems) {
        const overlay = (<Menu className={styles.OptionsMenu}
                               onClick={(e)=>props.optionsMenuClickHandler(e)}>{props.optionsMenuItems}
                        </Menu>);
        optionsMenu = (
            <div className={styles.Options}>
                <Dropdown overlay={overlay}>
                    <p>...</p>
                </Dropdown>
            </div>
        )
    }
    return (
        <div className={styles.Box}>
            {optionsMenu}


            <div className={styles.Body} onClick={() => props.onClick()}>
                <div className={styles.Icon}
                     style={{top: props.iconTop,
                            right: props.iconRight,
                            width: props.iconWidth || 90,
                            height: props.iconHeight || 90,
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
