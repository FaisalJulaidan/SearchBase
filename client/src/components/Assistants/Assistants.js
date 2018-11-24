import React, {Component} from 'react';


import "./Assistants.less"

import Assistant from "../Assistant/Assistant"

class Assistants extends Component {
    state = {};
    arr = Array(10).fill(0);

    render() {
        return (
            <div>
                <h1>Assistants List</h1>
                <hr/>
                {this.arr.map((x, i) => <Assistant key={i} index={i}/>)}
            </div>
        );
    }
}

export default Assistants;
