import React from 'react'
import styles from './Button.module.css'

import {default as AntdButton} from 'antd/lib/button';
import Icon from 'antd/lib/icon';

const Button = (props) => {
    const btnColor = !!props.btnColor ? props.btnColor : null;
    const styling = {
        width: '50px',
        height: '50px',
        boxShadow: '0px 2px 20px -4.5px #666',
        backgroundColor: btnColor,
        borderColor: btnColor
    };
    const isWaiting = props.isWaiting;
    return (
        <div className={`${styles.Button} ${styles.BounceIn}`}>
            {isWaiting ?
                <AntdButton
                    onClick={props.clicked}
                    type="primary"
                    shape="circle" size="large"
                    ghost={props.disabled}
                    disabled={props.disabled}
                    style={styling}>

                    <Icon type="message" theme="outlined"
                          style={{fontSize: '25px', margin: '11px 2px'}}/>
                </AntdButton>
                :
                <AntdButton type="primary" style={styling} shape="circle" loading
                            ghost={props.disabled}
                            disabled={props.disabled}/>
            }
        </div>
    );

}

export default Button
