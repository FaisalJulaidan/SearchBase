import React, {Component} from 'react';
import {connect} from 'react-redux';
import styles from "./Campaigns.module.less";
import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import {Icon, Typography, Menu, Modal} from 'antd';
import CreateNewBox from "components/CreateNewBox/CreateNewBox";
import ViewBox from "components/ViewBox/ViewBox";
import LoadingViewBox from "components/LoadingViewBox/LoadingViewBox";
import {AutoPilotIcon} from "components/SVGs";
import {history} from "helpers";
import {campaignActions} from "store/actions";

const {Title, Paragraph} = Typography;

class Campaigns extends Component {

    componentDidMount() {
        this.props.dispatch(campaignActions.fetchCampaigns())
    }

    deleteCampaign = (campaignID) => {
        Modal.confirm({
            title: `Delete campaign confirmation`,
            content: `If you click OK, this campaign will be deleted.`,
            onOk: () => {
                console.log(this.props);
                //TODO::
                // this.props.dispatch(campaignActions.deleteCampaign(campaignID))
            }
        });
    };

    optionsMenuClickHandler = (e, campaign) => {
        if (e.key === 'edit')
            history.push(`/dashboard/campaigns/${campaign.ID}`);
        if (e.key === 'delete')
            this.deleteCampaign(campaign.ID)
    };

    // it must be an array of Menu.Item. ViewBox expect that in its options Menu
    optionsMenuItems = [
        <Menu.Item style={{padding: 10, paddingRight: 30}} key="edit">
            <Icon type="edit" theme="twoTone" twoToneColor="#595959" style={{marginRight: 5}}/>
            Edit
        </Menu.Item>,
        <Menu.Item style={{padding: 10, paddingRight: 30}} key="delete">
            <Icon type="delete" theme="twoTone" twoToneColor="#f50808"/>
            Delete
        </Menu.Item>
    ];

    render() {
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <Title className={styles.Title}>
                            <Icon type="rocket"/> Campaign
                        </Title>
                        <Paragraph type="secondary">
                            Here you can use our Outreach engine to Engage with the candidates inside your CRM via SMS
                            and Email
                        </Paragraph>
                    </div>

                    <div className={styles.Body}>
                        <CreateNewBox text={'Add Campaign'}
                                      onClick={() => {
                                          history.push(`/dashboard/campaigns/new`)
                                      }}
                        />

                        {
                            this.props.isLoading ? <LoadingViewBox/>
                                :
                                this.props.campaignsList.map(
                                    (/**@type campaignsList*/ campaign, i) =>
                                        <ViewBox
                                            onClick={() => history.push(`/dashboard/campaigns/${campaign.ID}`)}
                                            optionsMenuItems={this.optionsMenuItems}
                                            optionsMenuClickHandler={(e) => this.optionsMenuClickHandler(e, campaign)}
                                            key={i}
                                            title={campaign.Name}
                                            text={campaign.Description}
                                            icon={<Icon type="rocket" style={{fontSize: '2em'}}/>}
                                            iconTop={175}
                                            iconRight={15}
                                        />
                                )
                        }
                    </div>
                </NoHeaderPanel>
            </>
        );
    }
}

function mapStateToProps(state) {
    return {
        campaignsList: state.campaign.campaignsList,
        isLoading: state.campaign.isLoading
    };
}

export default connect(mapStateToProps)(Campaigns);