import React, {Component, lazy, Suspense} from 'react';

import {Avatar, Dropdown, Icon, Layout, Menu} from 'antd';
import "./Dashboard.less"
import styles from "./Dashboard.module.less"

import {getUser, history} from "helpers";
import {Route, Switch, withRouter} from 'react-router-dom';
import {authActions, optionsActions} from "store/actions";
import {store} from "store/store";
import {connect} from 'react-redux';

import {CSSTransition, TransitionGroup} from "react-transition-group";

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faCloud} from '@fortawesome/free-solid-svg-icons'

const Home = lazy(() => import('./Home/Home'));
const Assistants = lazy(() => import('./Assistants/Assistants'));
const Assistant = lazy(() => import('./Assistants/Assistant/Assistant'));
const Databases = lazy(() => import('./Databases/Databases'));
const Database = lazy(() => import('./Databases/Database/Database'));
const Account = lazy(() => import('./ControlPanel/Account/Account'));
const Billing = lazy(() => import('./ControlPanel/Billing/Billing'));
const UsersManagement = lazy(() => import('./ControlPanel/UsersManagement/UsersManagement'));
const Documentation = lazy(() => import('./Documentation/Documentation'));
const Calendar = lazy(() => import('./Calendar/Calendar'));
const Campaign = lazy(() => import('./Campaign/Campaign'));
const AutoPilots = lazy(() => import('./AutoPilots/AutoPilots'));
const AutoPilot = lazy(() => import('./AutoPilots/AutoPilot/AutoPilot'));
const Marketplace = lazy(() => import('./Marketplace/Marketplace'));
const Item = lazy(() => import('./Marketplace/Item/Item'));


const {SubMenu} = Menu;
const {Divider} = Menu;
const {Header, Content, Footer, Sider} = Layout;


class Dashboard extends Component {
    state = {
        collapsed: false,
    };

    componentWillMount() {
        this.props.dispatch(optionsActions.getOptions())
    }


    toggle = () => {
        this.setState({
            collapsed: !this.state.collapsed,
        }, () => this.setState({marginLeft: this.state.collapsed ? 81 : 200}));
    };

    handleMenuClick = (e) => {
        if (e.key === 'logout') {
            return this.logout()
        }
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

        const {match, location} = this.props;
        const user = getUser();
        let userInfo = null;
        // User Information at the top
        if (!user) {
            this.logout();
        } else {

            let avatar = (
                <Avatar size="large" style={{backgroundColor: '#9254de', verticalAlign: 'middle'}}>
                    {this.getInitials(user.username || '')}
                </Avatar>
            );
            let userInfoMenu = (
                <Menu onClick={this.handleMenuClick}>
                    <Menu.Item key="account">
                        <div style={{display: 'flex', marginTop: '10px'}}>
                            {avatar}
                            <div style={{marginLeft: '10px'}}>
                                <h3>{user.username}</h3>
                                <p>{user.email}</p>
                            </div>
                        </div>
                    </Menu.Item>
                    <Menu.Divider/>
                    <Menu.Item key="logout">
                        <Icon type="logout"/>
                        <span>Logout</span>
                    </Menu.Item>
                </Menu>
            );
            userInfo = (
                <Dropdown overlay={userInfoMenu} overlayStyle={{width: '255px'}}>
                    {avatar}
                </Dropdown>
            );
        }
        // End of User Information

        const newLayoutRoutes = [
            "/dashboard/assistants",
            "/dashboard/marketplace",
            "/dashboard/calendar",
            "/dashboard/auto_pilot",
            "/dashboard/databases",
            "/dashboard/account",
            "/dashboard/users_management",
            "/dashboard/campaign"
        ];
        const isNewLayout = newLayoutRoutes.some(a => this.props.location.pathname.indexOf(a) > -1);
        return (
            <Layout style={{height: '100%'}}>
                <Sider
                    trigger={null}
                    collapsible
                    collapsed={this.state.collapsed}
                    style={{
                        // backgroundColor: isNewLayout ? '#20252e' : ''
                    }}

                    className={styles.Sider}>

                    <div className={styles.Logo}>
                        {
                            this.state.collapsed ?
                                <div style={{display: 'flex'}}>
                                    <FontAwesomeIcon size="2x" icon={faCloud}
                                                     style={{color: '#9254de', marginLeft: 7}}/>
                                </div>
                                :
                                <div style={{display: 'flex'}}>
                                    <FontAwesomeIcon size="2x" icon={faCloud} style={{color: '#9254de'}}/>
                                    <div style={{
                                        lineHeight: '32px',
                                        marginLeft: 18,
                                        // color: isNewLayout ? 'white' : '#9254de'
                                        color: "#9254de"
                                    }}>TheSearchBase
                                    </div>
                                </div>
                        }

                    </div>

                    <Menu
                        // theme={isNewLayout ? "dark" : "light"}
                        theme={"light"}
                        defaultSelectedKeys={this.state.selectedMenuKey}
                        selectedKeys={location.pathname.split('/')[2] ? [location.pathname.split('/')[2]] : [location.pathname.split('/')[1]]}
                        mode="inline" onClick={this.handleMenuClick}>
                        <Menu.Item key="dashboard">
                            <Icon type="home"/>
                            <span>Home</span>
                        </Menu.Item>

                        <Menu.Item key="assistants">
                            <Icon type="robot"/>
                            <span>Assistants</span>
                        </Menu.Item>

                        <Menu.Item key="campaign">
                            <Icon type="rocket"/>
                            <span>Campaign</span>
                        </Menu.Item>

                        <Menu.Item key="auto_pilots">
                            <Icon type="clock-circle"/>
                            <span>Auto Pilot</span>
                        </Menu.Item>

                        <Menu.Item key="marketplace">
                            <Icon type="interation"/>
                            <span>Marketplace</span>
                        </Menu.Item>

                        <Menu.Item key="databases">
                            <Icon type="database"/>
                            <span>Database</span>
                        </Menu.Item>

                        <Menu.Item disabled={true} key="calendar">
                            <Icon type="calendar"/>
                            <span>Calendar (soon)</span>
                        </Menu.Item>


                        <Divider/>

                        <SubMenu key="sub2" title={<span><Icon type="user"/><span>Control Panel</span></span>}>
                            <Menu.Item key="account">
                                <Icon type="profile"/>
                                Account
                            </Menu.Item>

                            {/*<Menu.Item key="billing">*/}
                            {/*<Icon type="pound"/>*/}
                            {/*Billing*/}
                            {/*</Menu.Item>*/}

                            <Menu.Item key="users_management">
                                <Icon type="usergroup-add"/>
                                Users
                            </Menu.Item>
                        </SubMenu>

                        <Menu.Item key="documentation">
                            <Icon type="question-circle"/>
                            <span>Documentation</span>
                        </Menu.Item>
                    </Menu>
                </Sider>

                <Layout style={
                    {marginLeft: this.state.collapsed ? 81 : 200, height: '100%'}}>

                    <Header className={styles.Header}
                            style={
                                isNewLayout ?
                                    {
                                        position: 'fixed',
                                        width: `calc(100% - ${this.state.collapsed ? 80 : 200}px)`,
                                    }
                                    :
                                    {}
                            }
                    >
                        <Icon className={styles.Trigger}
                              type={this.state.collapsed ? 'menu-unfold' : 'menu-fold'}
                              onClick={this.toggle}
                        />
                        <div className={styles.UserInfo}>
                            {userInfo}
                        </div>
                    </Header>

                    {/*HERE GOES ALL THE ROUTES*/}

                    <Content style={
                        isNewLayout ?
                            {minHeight: 'auto', marginTop: 64}
                            :
                            {margin: 16, marginTop: 10, marginBottom: 0, height: '100%'}
                    }>
                        <Route render={() =>
                            <TransitionGroup style={{height: '100%'}}>
                                <CSSTransition key={location.key} classNames="fade" timeout={550}>
                                    <Suspense fallback={<div> Loading...</div>}>
                                        <Switch location={location} style={{height: '100%'}}>

                                            <Route path={`${match.path}/assistants`} component={Assistants} exact/>
                                            <Route path={`${match.path}/assistants/:id`} component={Assistant} exact/>

                                            <Route path={`${match.path}/marketplace`} component={Marketplace} exact/>
                                            <Route path={`${match.path}/marketplace/:type`} component={Item} exact/>

                                            <Route path={`${match.path}/databases`} component={Databases} exact/>
                                            <Route path={`${match.path}/databases/:id`} component={Database} exact/>

                                            <Route path={`${match.path}/account`} component={Account} exact/>
                                            <Route path={`${match.path}/billing`} component={Billing} exact/>

                                            <Route path={`${match.path}/auto_pilots`} component={AutoPilots} exact/>
                                            <Route path={`${match.path}/auto_pilots/:id`} component={AutoPilot} exact/>

                                            <Route path={`${match.path}/users_management`} component={UsersManagement}
                                                   exact/>
                                            <Route path={`${match.path}/documentation`} component={Documentation}
                                                   exact/>
                                            {/*<Route path={`${match.path}/calendar`} component={Calendar} exact/>*/}

                                            <Route path={`${match.path}/campaign`} component={Campaign} exact/>

                                            <Route path="/dashboard" component={Home}/>
                                        </Switch>
                                    </Suspense>
                                </CSSTransition>
                            </TransitionGroup>
                        }/>
                    </Content>

                    <Footer style={{textAlign: 'center', padding: 10, zIndex: 1}}>
                        Copyright TheSearchBase Limited 2019. All rights reserved.
                    </Footer>
                </Layout>
            </Layout>
        );
    }
}

function mapStateToProps(state) {
    return {
        account: state.account.account
    };
}

export default withRouter(connect(mapStateToProps)(Dashboard));
