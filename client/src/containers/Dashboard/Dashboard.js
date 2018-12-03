import React, {Component} from 'react';

import {Icon, Layout, Menu} from 'antd';
import "./Dashboard.less"
import styles from "./Dashboard.module.less"
import Assistants from "../../components/Assistants/Assistants";
import store from '../../store/store'
import {connect} from 'react-redux';

const {SubMenu} = Menu;
const {Divider} = Menu;

const {Header, Content, Footer, Sider} = Layout;


const action = type => store.dispatch({type});

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

    render() {
        return (
            <Layout style={{height: '100%'}}>
                <Sider
                    trigger={null}
                    collapsible
                    collapsed={this.state.collapsed}
                    className={styles.Sider}>

                    <div className={styles.Logo}/>

                    <Menu theme="light" defaultSelectedKeys={['1']} mode="inline">
                        <Menu.Item key="1">
                            <Icon type="home"/>
                            <span>Home</span>
                        </Menu.Item>

                        <Menu.Item key="2">
                            <Icon type="robot"/>
                            <span>Assistants</span>
                        </Menu.Item>

                        <Divider/>

                        <SubMenu key="sub2"
                                 title={<span><Icon type="user"/><span>Account Detail</span></span>}>
                            <Menu.Item key="3">
                                <Icon type="profile"/>
                                Profile
                            </Menu.Item>
                            <Menu.Item key="4" style={{fontSize: '9pt'}}>
                                <Icon type="usergroup-add"/>Users Managment
                            </Menu.Item>
                        </SubMenu>

                        <Menu.Item key="5">
                            <Icon type="dollar"/>
                            <span>Billing</span>
                        </Menu.Item>
                        <Menu.Item key="6">
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

                        <Assistants/>
                        {/*<Flow/>*/}


                    </Content>

                    <Footer style={{textAlign: 'center', padding: 10}}>
                        The Search Base ©2018
                    </Footer>
                </Layout>
            </Layout>
        );
    }

}

const mapStateToProps = state => {
    return {
        counter: state.counter
    }
};
export default connect(mapStateToProps)(Dashboard);
