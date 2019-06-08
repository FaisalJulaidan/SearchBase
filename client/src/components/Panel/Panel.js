import React from 'react';
import {Spin} from 'antd';

import styles from "./Panel.module.less";
import PropTypes from 'prop-types';


// Not complete yet...
const Panel = (props) => {
    const TitleElement = React.Children.only(props.children[0]);
    const BodyElement = React.Children.only(props.children[1]);

    return (
        props.loading ?
            <Spin/>
            :
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        {React.cloneElement(TitleElement)}
                    </div>
                    <div className={styles.Panel_Body}>
                        {React.cloneElement(BodyElement)}
                    </div>
                </div>
            </div>
    );

};

Panel.propTypes = {
    title: PropTypes.string,
};

export default Panel;
