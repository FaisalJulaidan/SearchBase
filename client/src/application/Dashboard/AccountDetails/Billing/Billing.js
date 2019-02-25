import React from 'react';
import {Form, Tabs} from "antd";
import {connect} from 'react-redux';
import {isEmpty} from "lodash";

import styles from "./Billing.module.less"
import "./Billing.less"

// import {profileActions} from "../../../../store/actions/profile.actions";
const TabPane = Tabs.TabPane;

class Billing extends React.Component {

    componentDidMount() {
        // this.props.dispatch(profileActions.getProfile());
    }

    render() {

        return (
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>Billing</h3>
                            <p>This page will help you understand and control what you pay to us.</p>
                        </div>
                    </div>

                    <div className={styles.Panel_Body} style={{overflowY: "auto"}}>
                        <div id="generic_price_table">
                            <section>
                                <div className="container" style={{textAlign: "center"}}>

                                    {/*BLOCK ROW START*/}
                                    <div className="row">

                                        <div className="col-md-4 priceBlockStyle">

                                            {/*PRICE CONTENT START*/}
                                            <div className="generic_content active clearfix">

                                                {/*HEAD PRICE DETAIL START*/}
                                                <div className="generic_head_price clearfix">

                                                    {/*HEAD CONTENT START*/}
                                                    <div className="generic_head_content clearfix">

                                                        {/*HEAD START*/}
                                                        <div className="head_bg"></div>
                                                        <div className="head">
                                                            <span>Standard</span>
                                                        </div>
                                                        {/*//HEAD END*/}

                                                    </div>
                                                    {/*//HEAD CONTENT END*/}

                                                    {/*PRICE START*/}
                                                    <div className="generic_price_tag clearfix">	
                                                        <span className="price">
                                                            <span className="sign">£</span>
                                                            <span className="currency">14</span>
                                                            <span className="cent">.99</span>
                                                            <span className="month">/Monthly</span>
                                                        </span>
                                                    </div>
                                                    {/*//PRICE END*/}

                                                </div>
                                                {/*//HEAD PRICE DETAIL END*/}

                                                {/*FEATURE LIST START*/}
                                                <div className="generic_feature_list">
                                                    <ul>
                                                        {/*<li><span>∞</span> Unlimited Usage</li>*/}
                                                        <li><span>∞</span> Conversations</li>
                                                        <li><span>CV</span> Storage</li>
                                                        <li><span>CRM</span> Integration</li>
                                                        <li><span>Custom</span> Chatbots</li>
                                                        <li><span>7 Day</span> Support</li>
                                                    </ul>
                                                </div>
                                                {/*//FEATURE LIST END*/}

                                                {/*BUTTON START*/}
                                                <div className="generic_price_btn clearfix">
                                                    <a className="" href="">Sign up</a>
                                                </div>
                                                {/*//BUTTON END*/}

                                            </div>
                                            {/*//PRICE CONTENT END*/}

                                        </div>
                                        <div className="col-md-4 priceBlockStyle">

                                            {/*PRICE CONTENT START*/}
                                            <div className="generic_content clearfix">

                                                {/*HEAD PRICE DETAIL START*/}
                                                <div className="generic_head_price clearfix">

                                                    {/*HEAD CONTENT START*/}
                                                    <div className="generic_head_content clearfix">

                                                        {/*HEAD START*/}
                                                        <div className="head_bg"></div>
                                                        <div className="head">
                                                            <span>Professional</span>
                                                        </div>
                                                        {/*//HEAD END*/}

                                                    </div>
                                                    {/*//HEAD CONTENT END*/}

                                                    {/*PRICE START*/}
                                                    <div className="generic_price_tag clearfix">	
                                                        <span className="price">
                                                            <span className="sign">£</span>
                                                            <span className="currency">129</span>
                                                            <span className="cent">.99</span>
                                                            <span className="month">/Annually</span>
                                                        </span>
                                                    </div>
                                                    {/*//PRICE END*/}

                                                </div>
                                                {/*//HEAD PRICE DETAIL END*/}

                                                {/*FEATURE LIST START*/}
                                                <div className="generic_feature_list">
                                                    <ul>
                                                        <li><span>∞</span> Unlimited Usage</li>
                                                        <li><span>∞</span> Conversations</li>
                                                        <li><span>CV</span> Storage</li>
                                                        <li><span>CRM</span> Integration</li>
                                                        <li><span>Custom</span> Chatbots</li>
                                                        <li><span>7 Day</span> Support</li>
                                                    </ul>
                                                </div>
                                                {/*//FEATURE LIST END*/}

                                                {/*BUTTON START*/}
                                                <div className="generic_price_btn clearfix">
                                                    <a className="" href="">Sign up</a>
                                                </div>
                                                {/*//BUTTON END*/}

                                            </div>
                                            {/*//PRICE CONTENT END*/}

                                        </div>

                                        <div className="col-md-4 priceBlockStyle">

                                            {/*PRICE CONTENT START*/}
                                            <div className="generic_content clearfix">

                                                {/*HEAD PRICE DETAIL START*/}
                                                <div className="generic_head_price clearfix">

                                                    {/*HEAD CONTENT START*/}
                                                    <div className="generic_head_content clearfix">

                                                        {/*HEAD START*/}
                                                        <div className="head_bg"></div>
                                                        <div className="head">
                                                            <span>Enterprise</span>
                                                        </div>
                                                        {/*//HEAD END*/}

                                                    </div>
                                                    {/*//HEAD CONTENT END*/}

                                                    {/*PRICE START*/}
                                                    <div className="generic_price_tag clearfix">
                                                        <span className="price">
                                                            <span className="sign"></span>
                                                            <span className="currency"></span>
                                                            <span className="cent">Contact Sales Team</span>
                                                            <span className="month"></span>
                                                        </span>
                                                    </div>
                                                    {/*//PRICE END*/}

                                                </div>
                                                {/*//HEAD PRICE DETAIL END*/}

                                                {/*FEATURE LIST START*/}
                                                <div className="generic_feature_list">
                                                    <ul>
                                                        <li><span>Access</span> to Personal Assistant</li>
                                                        <li><span>∞</span> Unlimited Usage</li>
                                                        <li><span>∞</span> Conversations</li>
                                                        <li><span>CV</span> Storage</li>
                                                        <li><span>CRM</span> Integration</li>
                                                        <li><span>Custom</span> Chatbots</li>
                                                        <li><span>7 Day</span> Support</li>
                                                    </ul>
                                                </div>
                                                {/*//FEATURE LIST END*/}

                                                {/*BUTTON START*/}
                                                <div className="generic_price_btn clearfix">
                                                    <a className="" href="mailto:info@thesearchbase.com?subject=Enterprise Package&body=Hi, I'm interested in the Enterprise Package.">Contact Sales</a>
                                                </div>
                                                {/*//BUTTON END*/}

                                            </div>
                                            {/*//PRICE CONTENT END*/}

                                        </div>
                                    </div>
                                    {/*//BLOCK ROW END*/}

                                </div>
                            </section>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        // profileData: state.profile.profile
    };
}

export default connect(mapStateToProps)(Form.create()(Billing));
