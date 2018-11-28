import React, {Component} from 'react';
import "./Flow.less"

import Groups from "./Groups/Groups";
import Blocks from "./Blocks/Blocks";
import Header from "./Header/Header";

/*
*
* Todo:
*   1- split Flow into components (DONE)
*   2- design card for each tab type
*   3- design add group modal (DONE)
*   5- Clean BlocksDrawer component (DONE)
* */

class Flow extends Component {


    render() {
        return (
            <div style={{height: '100%'}}>

                <div style={{padding: '0 5px'}}>
                    <div style={{width: '100%', height: 56, marginBottom: 10}}>
                        <Header/>
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

