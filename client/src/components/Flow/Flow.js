import React, {Component} from 'react';
import "./Flow.less"

import Groups from "./Groups/Groups";
import Blocks from "./Blocks/Blocks";
import Header from "./Header/Header";

/*
*
* Todo:
*   2- design card for each tab type
*   3- design add group modal
* */

class Flow extends Component {


    render() {
        const {assistant} = this.props.location.state;
        console.log(assistant)

        return (
            <div style={{height: '100%'}}>

                <div style={{padding: '0 5px'}}>
                    <div style={{width: '100%', height: 56, marginBottom: 10}}>
                        <Header assistantName={assistant.Name}/>
                    </div>
                </div>

                <div style={{height: 'calc(100% - 66px)', width: '100%', display: 'flex'}}>
                    <div style={{margin: 5, width: '30%'}}>
                        <Groups/>
                    </div>

                    <div style={{margin: 5, width: '70%'}}>
                        <Blocks/>
                    </div>
                </div>
            </div>
        );
    }

}

export default Flow;

