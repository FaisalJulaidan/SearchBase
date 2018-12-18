import React from 'react';
import {Button} from "antd";

export default class CustomAnchor extends React.Component {

    openLink(link){
        window.open(link,"_self")
    }


    render(){
        return (
            <Button style={{marginLeft: "6px"}} className={"ant-btn-primary"} onClick={() => {this.openLink(this.props.route)}}>{this.props.children}</Button>
        )
    }
}