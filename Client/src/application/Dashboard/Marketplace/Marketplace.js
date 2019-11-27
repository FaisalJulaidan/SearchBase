import React from 'react'
import {Icon, Typography} from 'antd';
import styles from './Marketplace.module.less'
import 'types/Marketplace_Types';
import data from './Items.json'
import AuroraCardAvatar from "components/AuroraCardAvatar/AuroraCardAvatar";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {history} from "helpers";

const {Title, Paragraph, Text} = Typography;

class Marketplace extends React.Component {

    render() {
        return (
            <NoHeaderPanel>
                <div className={styles.Header}>
                    <Title className={styles.Title}>
                        <Icon type="shop"/> Marketplace
                    </Title>
                    <Paragraph type="secondary">
                        We integrate with a range of CRM, ATS, Calendars and Messaging Services.
                        From the list below, choose the one you want for your account to be directly connected with.
                        If you need help with the setup or wish to contact us to arrange an integration with
                        your provider, please contact us at:
                        <Text code>
                            <a target={'_blank'} href={"mailto:info@thesearchbase.com"} style={{cursor: 'pointer'}}>
                                info@thesearchbase.com
                            </a>
                        </Text>.
                    </Paragraph>
                </div>

                <div className={styles.Body}>
                    {
                        data.Items.map((item, i) =>
                            <div className={styles.CardFrame} key={i}>
                                <AuroraCardAvatar
                                    onClick={() => history.push(`/dashboard/marketplace/${item.type}`)}
                                    title={item.title}
                                    desc={item.desc}
                                    image={item.image}
                                    disabled={item.disabled}/>
                            </div>
                        )
                    }
                </div>
            </NoHeaderPanel>
        )
    }
}

export default Marketplace;
