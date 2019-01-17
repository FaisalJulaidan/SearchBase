import React, {Component} from 'react';

import {Avatar, Dropdown, Icon, Layout, Menu} from 'antd';
import "./Dashboard.less"
import styles from "./Dashboard.module.less"
import Assistants from './Assistants/Assistants';
import {getUser, history} from '../../helpers';
import {Route, Switch} from 'react-router-dom';
import Flow from "./Assistants/Assistant/Flow/Flow";
import Profile from "./Profile/Profile";
import Integration from "./Assistants/Assistant/Integration/Integration";
import UserInput from "./Assistants/Assistant/UserInput/UserInput";
import Solutions from "./Assistants/Assistant/Solutions/Solutions";
import Home from "./Home/Home";
import {authActions} from "../../store/actions";
import store from '../../store/store';
import {connect} from 'react-redux';


const {SubMenu} = Menu;
const {Divider} = Menu;
const {Header, Content, Footer, Sider} = Layout;


class Dashboard extends Component {
    state = {
        collapsed: false,
        marginLeft: 200,
    };

    toggle = () => {
        this.setState({
            collapsed: !this.state.collapsed,
        }, () => this.setState({marginLeft: this.state.collapsed ? 81 : 200}));
    };

    handleMenuClick = (e) => {
        if (e.key === 'logout'){this.logout()}
        e.key === 'dashboard' ? history.push(`/dashboard`) : history.push(`/dashboard/${e.key}`)
    };

    logout = () => {
        store.dispatch(authActions.logout());
    };

    getInitials = (username) => {
        const initials = username.match(/\b\w/g) || [];
        return ((initials.shift() || '') + (initials.pop() || '')).toUpperCase();
    };

    render() {

        const {match} = this.props;
        const user = getUser();
        let userInfo = null;

        // User Information at the top
        if (!user) {
            this.logout();
        } else {

            let avatar = (
                <Avatar size="large" style={{ backgroundColor: '#9254de', verticalAlign: 'middle' }}>
                    {this.getInitials(user.username || '')}
                </Avatar>
            );
            let userInfoMenu = (
                <Menu onClick={this.handleMenuClick}>
                    <Menu.Item key="profile">
                        <div style={{display:'flex', marginTop:'10px'}}>
                            {avatar}
                            <div style={{marginLeft:'10px'}}>
                                <h3>{user.username}</h3>
                                <p>{user.email}</p>
                            </div>
                        </div>
                    </Menu.Item>
                    <Menu.Divider />
                    <Menu.Item key="logout" >
                        <Icon type="logout"/>
                        <span>Logout</span>
                    </Menu.Item>
                </Menu>
            );

            userInfo = (
                <Dropdown overlay={userInfoMenu} overlayStyle={{width:'255px'}}>
                    {avatar}
                </Dropdown>
            );
        }
        // End of User Information


        return (
            <Layout style={{height: '100%'}}>
                <Sider
                    trigger={null}
                    collapsible
                    collapsed={this.state.collapsed}
                    className={styles.Sider}>

                    <div className={styles.Logo}>
                        <div style={{display: 'flex'}}>
                            <Icon type="cloud" theme="twoTone" twoToneColor="#9254de" style={{fontSize: 44}}/>
                            <div style={{lineHeight: '43px', marginLeft: 25}}>TheSearchBase</div>
                        </div>
                    </div>

                    <Menu theme="light" defaultSelectedKeys={['dashboard']} mode="inline" onClick={this.handleMenuClick}>
                        <Menu.Item key="dashboard">
                            <Icon type="home"/>
                            <span>Home</span>
                        </Menu.Item>

                        <Menu.Item key="assistants">
                            <Icon type="robot"/>
                            <span>Assistants</span>
                        </Menu.Item>

                        <Divider/>

                        <SubMenu key="sub2"
                                 title={<span><Icon type="user"/><span>Account Details</span></span>}>
                            <Menu.Item key="profile">
                                <Icon type="profile"/>
                                Profile
                            </Menu.Item>
                            <Menu.Item key="users-management" style={{fontSize: '9pt'}}>
                                <Icon type="usergroup-add"/>Users Management
                            </Menu.Item>
                        </SubMenu>

                        {/*<Menu.Item key="billing">*/}
                            {/*<Icon type="dollar"/>*/}
                            {/*<span>Billing</span>*/}
                        {/*</Menu.Item>*/}
                        <Menu.Item key="support">
                            <Icon type="question-circle"/>
                            <span>Support</span>
                        </Menu.Item>
                    </Menu>
                </Sider>

                <Layout style={{marginLeft: this.state.marginLeft, height: '100%'}}>

                    <Header className={styles.Header}>
                        <Icon
                            className={styles.Trigger}
                            type={this.state.collapsed ? 'menu-unfold' : 'menu-fold'}
                            onClick={this.toggle}
                        />
                        <div className={styles.UserInfo}>
                            {userInfo}
                        </div>
                    </Header>

                    {/*HERE GOES ALL THE ROUTES*/}
                    <Content style={{margin: 16, marginTop: 10, marginBottom: 0, height: '100%'}}>
                        <Switch>
                            <Route path={`${match.path}/assistants/:id/flow`} component={Flow}/>
                            <Route path={`${match.path}/assistants/:id/integration`} component={Integration}/>
                            <Route path={`${match.path}/assistants/:id/userInput`} component={UserInput}/>
                            <Route path={`${match.path}/assistants/:id/solutions`} component={Solutions}/>
                            <Route path={`${match.path}/assistants`} component={Assistants} exact/>
                            <Route path={`${match.path}/profile`} component={Profile} exact/>
                            <Route path="/dashboard" component={Home}/>
                        </Switch>
                    </Content>

                    <Footer style={{textAlign: 'center', padding: 10}}>
                        Copyright TheSearchBase Limited 2019. All rights reserved.
                    </Footer>
                </Layout>
            </Layout>
        );
    }
}

function mapStateToProps(state) {
    return {
        profile: state.profile.profile
    };
}

export default connect(mapStateToProps)(Dashboard);