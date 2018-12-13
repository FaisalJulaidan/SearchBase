import React, {Component} from 'react';

import "./Profile.less"
import styles from "./Profile.module.less"

class Profile extends Component {
    state = {};

    render() {
        return (
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>User Profile</h3>
                            <p>Here you can edit your profile configs</p>
                        </div>
                    </div>


                    <div className={styles.Panel_Body}>
                        {/*Here you add the components*/}
                        <h3>Profile component works</h3>
                        <p>You need to add components from ant-design</p>
                    </div>
                </div>
            </div>

        );
    }

}

export default Profile;
