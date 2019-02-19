import React from 'react';
import {Form, Button, message, Tabs} from "antd";
import {connect} from 'react-redux';
import {isEmpty} from "lodash";

import styles from "./Billing.module.less"

// import {profileActions} from "../../../../store/actions/profile.actions";
const TabPane = Tabs.TabPane;

class Billing extends React.Component {

    componentDidMount() {
        // this.props.dispatch(profileActions.getProfile());
    }

    render() {

        return (
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>Billing</h3>
                            <p>This page will help you understand and control what you pay to us.</p>
                        </div>
                    </div>

                    <div className={styles.Panel_Body} style={{overflowY: "auto"}}>

                    </div>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        // profileData: state.profile.profile
    };
}

export default connect(mapStateToProps)(Form.create()(Billing));
