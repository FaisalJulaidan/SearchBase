import React, {Component} from 'react';

import {Icon, Layout, Menu} from 'antd';
import "./Dashboard.less"
import styles from "./Dashboard.module.less"
import Assistants from './Assistants/Assistants';
import {history} from '../../helpers';
import {Switch, Route} from 'react-router-dom';
import Flow from "./Assistants/Assistant/Flow/Flow";
import Profile from "./Profile/Profile";
import Integration from "./Assistants/Assistant/Integration/Integration";

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
        e.key === 'dashboard' ? history.push(`/dashboard`) : history.push(`/dashboard/${e.key}`)
    };

    render() {
        const {match} = this.props;
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

                    <Menu theme="light" defaultSelectedKeys={['1']} mode="inline" onClick={this.handleMenuClick}>
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

                        <Menu.Item key="billing">
                            <Icon type="dollar"/>
                            <span>Billing</span>
                        </Menu.Item>
                        <Menu.Item key="support">
                            <Icon type="question-circle"/>
                            <span>Support</span>
                        </Menu.Item>
                    </Menu>
                </Sider>

                <Layout style={{marginLeft: this.state.marginLeft, height: '100%'}}>

                    <Header className={styles.Header}>
                        <Icon
                            className={styles.trigger}
                            type={this.state.collapsed ? 'menu-unfold' : 'menu-fold'}
                            onClick={this.toggle}
                        />
                    </Header>

                    {/*HERE GOES ALL THE ROUTES*/}
                    <Content style={{margin: 16, marginTop: 80, marginBottom: 0, height: '100%'}}>

                        <Switch>
                            <Route path={`${match.path}/assistants/:id/flow`} component={Flow}/>
                            <Route path={`${match.path}/assistants`} component={Assistants} exact/>
                            <Route path={`${match.path}/profile`} component={Profile} exact/>
                            <Route path={`${match.path}/integration/:id`} component={Integration}/>

                            {/*<Route path="/dashboard" component={Dashboard}/>*/}
                        </Switch>
                    </Content>

                    <Footer style={{textAlign: 'center', padding: 10}}>
                        The Search Base ©2018
                    </Footer>
                </Layout>
            </Layout>
        );
    }

}

export default Dashboard;
