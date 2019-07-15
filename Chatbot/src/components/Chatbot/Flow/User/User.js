import React from "react";
import styles from "./User.module.css";
import {Row} from "antd";

const User = (props) => {
    let isIE11 = !!window.MSInputMethodContext && !!document.documentMode;
    let isEdge = /Edge/.test(navigator.userAgent);
    return <Row>
        <div className={[isIE11 || isEdge ? styles.User_IE11 : styles.User, styles.bounceIn].join(' ')}>
            <p>
                {props.text}
            </p>
        </div>
    </Row>
};


export default User;