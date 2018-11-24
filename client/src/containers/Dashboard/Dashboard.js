import React, {Component} from 'react';

import {Breadcrumb, Icon, Layout, Menu} from 'antd';
import "./Dashboard.less"
import styles from "./Dashboard.module.less"

import Assistants from '../../components/Assistants/Assistants'

const {Header, Content, Footer, Sider} = Layout;

class Dashboard extends Component {
    state = {
        collapsed: false,
        marginLeft: 200
    };

    toggle = () => {
        this.setState({
            collapsed: !this.state.collapsed,
        }, () => this.setState({marginLeft: this.state.collapsed ? 80 : 200}));
    };


    render() {
        return (
            <Layout style={{height: '100%'}}>
                <Sider
                    trigger={null}
                    collapsible
                    collapsed={this.state.collapsed}
                    className={styles.Sider}
                >
                    <div className={styles.Logo}/>

                    <Menu theme="light" defaultSelectedKeys={['1']} mode="inline">
                        <Menu.Item key="1">
                            <Icon type="pie-chart"/>
                            <span>Option 1</span>
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

                    <Content style={{margin: 16, marginTop: 80, marginBottom: 0, height: '100%'}}>
                        <Breadcrumb>
                            <Breadcrumb.Item href="">
                                <Icon type="home"/>
                            </Breadcrumb.Item>

                            <Breadcrumb.Item>
                                Assistants
                            </Breadcrumb.Item>
                        </Breadcrumb>
                        <br/>
                        <div style={{padding: 24, background: '#fff', overflowY: 'auto', height: '100%'}}>
                            <Assistants/>
                        </div>
                    </Content>

                    <Footer style={{textAlign: 'center', padding: 10}}>
                        Ant Design ©2018 Created by Ant UED
                    </Footer>
                </Layout>
            </Layout>
        );
    }
}

export default Dashboard;
