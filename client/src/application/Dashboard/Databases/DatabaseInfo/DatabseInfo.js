import React, {Component} from 'react';
import Handsontable from 'handsontable';
import {HotTable} from "@handsontable/react";
import './DatabaseInfo.less'
import {ColumnsOptions} from "../NewDatabaseModal/ColumnsOptions";

class DatabseInfo extends Component {

    render() {

        let data = this.props.data;
        const columns = this.props.databaseOption[this.props.databaseInfo.Type].map(x => x.column);
        const colHeaders = this.props.databaseOption[this.props.databaseInfo.Type].map(x => x.column).map(x => {
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


export default DatabseInfo;