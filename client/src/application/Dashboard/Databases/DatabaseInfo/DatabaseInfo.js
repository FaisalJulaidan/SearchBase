import React, {Component} from 'react';
import Handsontable from 'handsontable';
import {HotTable} from "@handsontable/react";
import './DatabaseInfo.less'
import {ColumnsOptions} from "../NewDatabaseModal/ColumnsOptions";

class DatabaseInfo extends Component {


    // handsontableData = Handsontable.helper.createSpreadsheetData(6, 10);


    render() {
        let handsontableData = this.props.data;
        let handsontableData1 = handsontableData.map(record => Object.values(record));
        // const handsontableColmns = this.props.data ? ColumnsOptions(handsontableData[0], 'handsontable') : [];
        console.log(handsontableData);
        return (
            <div style={{height: '100%'}}>
                <HotTable id="hot"
                          data={handsontableData1}
                          colHeaders={Object.keys(handsontableData[0])}
                          rowHeaders={true}/>

            </div>
        );
    }
}


export default DatabaseInfo;