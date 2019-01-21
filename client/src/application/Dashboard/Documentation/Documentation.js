import React from "react";
import Header from "../../../components/Header/Header";
import SolutionsDisplay from "../Assistants/Assistant/Solutions/SolutionsDisplay/SolutionsDisplay";
import SolutionsSettings from "../Assistants/Assistant/Solutions/SolutionsSettings/SolutionsSettings";
import { Menu, Icon } from 'antd';

const SubMenu = Menu.SubMenu;

class Documentation extends React.Component{

    state = {
        currentKey: "1"
    };

    handleMenuChange = (item) => {
        console.log(item)
    };

    render () {


        return (
            <div style={{height: '100%'}}>
                <div style={{padding: '0 5px'}}>
                    <div style={{width: '100%', height: 56, marginBottom: 10}}>
                        <Header display={"Solutions"}/>
                    </div>
                </div>

                <div style={{height: 'calc(100% - 66px)', width: '100%', display: 'flex'}}>
                    <div style={{margin: 5, width: '27%'}}>

                        <Menu
                            mode="inline"
                            style={{ width: 256 }}
                            onClick={this.handleMenuChange}
                          >
                            <SubMenu key="sub1" title={<span><Icon type="mail" /><span>Navigation One</span></span>}>
                              <Menu.Item key="1">Option 1</Menu.Item>
                              <Menu.Item key="2">Option 2</Menu.Item>
                              <Menu.Item key="3">Option 3</Menu.Item>
                              <Menu.Item key="4">Option 4</Menu.Item>
                            </SubMenu>

                            <SubMenu key="sub2" title={<span><Icon type="appstore" /><span>Navigation Two</span></span>}>
                              <Menu.Item key="5">Option 5</Menu.Item>
                              <Menu.Item key="6">Option 6</Menu.Item>
                            </SubMenu>

                            <SubMenu key="sub4" title={<span><Icon type="setting" /><span>Navigation Three</span></span>}>
                              <Menu.Item key="9">Option 9</Menu.Item>
                              <Menu.Item key="10">Option 10</Menu.Item>
                              <Menu.Item key="11">Option 11</Menu.Item>
                              <Menu.Item key="12">Option 12</Menu.Item>
                            </SubMenu>
                          </Menu>

                    </div>

                    <div style={{margin: 5, width: '73%'}}>



                    </div>
                </div>
            </div>
        )
    }
}

export default Documentation