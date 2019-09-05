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

    render() {
        return (
            <>
                <NoHeaderPanel>
                    <div className={styles.Header}>
                        <Title className={styles.Title}>
                            <Icon type="interation"/> Campaign
                        </Title>
                        <Paragraph type="secondary">
                            Here you can use our Outreach engine to Engage with the candidates inside your CRM via SMS and Email
                        </Paragraph>
                    </div>

                    <div className={styles.Body}>
                        <CreateNewBox text={'Add Campaign'}
                                      // onClick={this.showNewAutoPilotModal}
                        />

                        {
                            this.props.isLoading ? <LoadingViewBox/>
                                :
                                this.props.campaignsList.map(
                                    (/**@type campaignsList*/ campaign, i) =>
                                        <ViewBox
                                            onClick={() => history.push(`/dashboard/campaigns/${campaign.ID}`)}
                                            optionsMenuItems={this.optionsMenuItems}
                                            optionsMenuClickHandler={(e)=>this.optionsMenuClickHandler(e, campaign)}
                                            key={i}
                                            title={campaign.Name}
                                            text={campaign.Description}
                                            icon={<AutoPilotIcon/>}
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