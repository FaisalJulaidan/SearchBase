import React from 'react'
import {Icon, Typography} from 'antd';
import styles from './Marketplaces.module.less'
import 'types/Marketplaces_Types';
import data from './Marketplaces.json'
import AuroraCardAvatar from "components/AuroraCardAvatar/AuroraCardAvatar";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Link} from "react-router-dom";

const {Title, Paragraph, Text} = Typography;

class Marketplaces extends React.Component {

    render() {
        return (
            <NoHeaderPanel>
                <div className={styles.Header}>
                    <Title className={styles.Title}>
                        <Icon type="interation"/> Marketplace
                    </Title>
                    <Paragraph type="secondary">
                        From the list below, choose your CRM or ATS for your account to be directly connected.
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
                        data.Marketplaces.map((marketplace, i) =>
                            <div className={styles.CardFrame} key={i}>
                                <Link to={{
                                    pathname: `/dashboard/marketplaces/${marketplace.type}`,
                                }}>
                                    <AuroraCardAvatar title={marketplace.title}
                                                      desc={marketplace.desc}
                                                      image={marketplace.image}
                                                      disabled={marketplace.disabled}/>
                                </Link>
                            </div>
                        )
                    }
                </div>
            </NoHeaderPanel>
        )
    }
}

export default Marketplaces;
