import {Table, Divider} from "antd";
import React, {Component} from 'react'
import {ColumnsOptions} from '../ColumnsOptions'

class ConfirmStep extends Component {

    getRecordsData = records => {
        let x = [];
        let counter = 0;
        for (const record of records) {
            let renderedRecord = {};
            renderedRecord.key = counter++;
            for (const key of Object.keys(record))
                renderedRecord[key] = record[key];
            x.push(renderedRecord);
        }
        return x;
    };

    render() {

        const {validRecords, invalidRecords} = this.props;
        const columnsOptions = ColumnsOptions(validRecords[0] || invalidRecords[0]);
        return (
            <div>
                <h4>Valid data </h4>
                <Table columns={columnsOptions}
                       dataSource={this.getRecordsData(validRecords)}
                       size="small"
                       pagination={{pageSize: 5}}/>

                <Divider/>

                <h4>Invalid data (wither fix them or upload without them) </h4>
                <Table columns={columnsOptions}
                       dataSource={this.getRecordsData(invalidRecords)}
                       size="small"
                       pagination={{pageSize: 5}}/>
            </div>
        )
    }
}

export default ConfirmStep;




