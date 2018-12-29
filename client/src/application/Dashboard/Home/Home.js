import React from 'react';
import "./Home.less"
import styles from "./Home.module.less"

class Home extends React.Component {

    state = {

    };

    render() {
        return (

            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>

                    </div>

                    <div className={styles.Panel_Body} style={{overflowY: "auto"}}>
                        <h1>Welcome to the Dashboard.</h1>
                        <h3>Use your side navigation to navigate the application.</h3>
                    </div>
                </div>

            </div>
        );
    }
}

export default Home;