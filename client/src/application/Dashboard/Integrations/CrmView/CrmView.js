import React from 'react'
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Typography, Avatar, Tabs} from 'antd';


import styles from './CrmView.module.less'
import {history} from "helpers";
import 'types/CRM_Types';

const TabPane = Tabs.TabPane;
const {Title, Paragraph, Text} = Typography;

class CrmView extends React.Component {


    state = {
        /** @type {CRM} */
        CRM: {}
    };

    componentDidMount() {

        this.setState({CRM: this.props.location?.state?.CRM}, () => {
            // If the state is not passed from the parent page redirect the user to integration page to
            // click on the needed CRM to show its data (or use its state)
            if (!this.state.CRM?.type)
                history.push('/dashboard/integrations')
        });
    }



    render() {
        return (
            <NoHeaderPanel>
                <div className={styles.Title}>
                    <Avatar shape="square" size={80} src={this.state.CRM.image} className={styles.Avatar}/>
                    <div className={styles.DetailsWithAvatar}>
                        <Title level={2}>{this.state.CRM?.type}</Title>
                        <Paragraph type="secondary">
                            We supply a series of design principles, practical patterns and high quality design
                            resources
                            (<Text code>Sketch</Text> and <Text code>Axure</Text>), to help people create their
                            product
                            prototypes beautifully and efficiently.
                        </Paragraph>
                    </div>
                </div>

                <div className={styles.Body}>
                    <Tabs defaultActiveKey="1">
                        <TabPane tab="Connection" key="1">Content of Tab Pane 1</TabPane>
                        <TabPane tab="Feature" key="2">Content of Tab Pane 2</TabPane>
                    </Tabs>

                </div>

            </NoHeaderPanel>
        );
    }
}

export default CrmView;
