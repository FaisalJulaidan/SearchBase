import React from "react";
import {Button, Switch} from "antd";
import styles from "../SolutionsSettings.module.less";

class EmailAutomatch extends React.Component {


    render() {

        return (
            <div style={{textAlign:"center"}}>

                <p>You can send emails to your clients when a new Solution suited for them has been added to your records.
                    This can be done manually by clicking the button bellow or by ticking the box which will check
                    and send them every time you update your data.</p>

                <Button onClick={this.props.sendSolutionAlerts} className={styles.Button} type={"primary"}>Send Matches</Button><br />

                <label>Automatic Matching on Record Update:</label><br />
                <Switch loading={false} checkedChildren={"On"} unCheckedChildren={"Off"} defaultChecked={false} onChange={this.props.submitAutomaticAlerts}/>


            </div>
        )
    }
}

export default EmailAutomatch