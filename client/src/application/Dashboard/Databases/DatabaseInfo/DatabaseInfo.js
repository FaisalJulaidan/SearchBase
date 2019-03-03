import React, {Component} from 'react';
import {HotTable} from "@handsontable/react";
import './DatabaseInfo.less'

class DatabaseInfo extends Component {

    render() {

        let data = this.props.data;

        const columns = this.props.databaseOptions[this.props.databaseInfo.Type.name].map(x => x.column);
        const colHeaders = this.props.databaseOptions[this.props.databaseInfo.Type.name].map(x => x.column).map(x => {
            return {
                data: x,
                editor: false
            }
        });
        return (
            <div style={{height: '100%'}}>
                <HotTable id="hot" data={data} colHeaders={columns} columns={colHeaders} rowHeaders={true}/>
            </div>
        );
    }
}


export default DatabaseInfo;