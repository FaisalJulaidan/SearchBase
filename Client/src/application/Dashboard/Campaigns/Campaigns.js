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
import {trimText} from "../../../helpers";

const {Title, Paragraph} = Typography;

class Campaigns extends Component {

    componentDidMount() {
        this.props.dispatch(campaignActions.fetchCampaigns())
    }

    deleteCampaign = (campaignID) => {
        Modal.confirm({
            title: 'Are you sure delete this campaign?',
            content: `If you click YES, this campaign data will be deleted.`,
            okText: 'Yes',
            okType: 'danger',
            cancelText: 'No',
            onOk: () => {
                this.props.dispatch(campaignActions.deleteCampaign(campaignID))
            }
        });
    };

    optionsMenuClickHandler = (e, campaign) => {
        switch (e.key) {
            case "edit":
                history.push(`/dashboard/campaigns/${campaign.ID}`);
                break;
            case "delete":
                this.deleteCampaign(campaign.ID)
                break;
        }
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
                            Here you can use our Outreach engine to Engage with the candidates inside your CRM via SMS and
                            Email. Campaigns are a great way for you to keep your CRM or database refreshed with GDPR compliant
                            information.
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
                                this.props.campaigns?.map(
                                    (/**@type campaignsList*/ campaign, i) =>
                                        <ViewBox
                                            onClick={() => history.push(`/dashboard/campaigns/${campaign.ID}`)}
                                            optionsMenuItems={this.optionsMenuItems}
                                            optionsMenuClickHandler={(e) => this.optionsMenuClickHandler(e, campaign)}
                                            key={i}
                                            title={trimText.capitalize(trimText.trimDash(campaign.Name))}
                                            text={trimText.capitalize(trimText.trimDash(campaign.Location))}
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
        campaigns: state.campaign.campaigns,
        isLoading: state.campaign.isLoading,
        isDeleting: state.campaign.isDeleting,
        errorMsg: state.campaign.errorMsg
    };
}

export default connect(mapStateToProps)(Campaigns);