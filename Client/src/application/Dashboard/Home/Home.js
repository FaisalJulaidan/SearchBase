import React from 'react';
import styles from "./Home.module.less"
import {getLink} from "helpers";

class Home extends React.Component {

    state = {

    };

    render() {
        return (

            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <h1>Welcome to the Dashboard</h1>
                    </div>

                    <div className={styles.Panel_Body}>
                        <h1>Welcome!</h1>
                        <img src={"/images/undraw/hello.svg"}
                             alt="welcome image"
                             width={300}/>
                        <h2>Here you can manage all your bots & see their usage analytics</h2>
                        <h4>Use your side navigation to navigate the application.</h4>
                    </div>
                </div>

            </div>
        );
    }
}

export default Home;
