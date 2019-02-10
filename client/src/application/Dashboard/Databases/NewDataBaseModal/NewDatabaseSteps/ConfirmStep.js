import {Table, Divider} from "antd";
import React, {Component} from 'react'
import {ColumnsOptions} from '../ColumnsOptions'

class ConfirmStep extends Component {

    getValidRecordsData = (records) => {
        let x = [];
        let counter = 0;
        for (const record of records) {
            let renderedRecord = {};
            renderedRecord.key = counter++;

            for (const key of Object.keys(record))
                renderedRecord[key] = record[key].data;

            x.push(renderedRecord);
        }
        return x;
    };


    render() {

        const {validRecords, invalidRecords} = this.props;
        const columnsOptions = ColumnsOptions(validRecords[0] || invalidRecords[0]);
        return (
            <div>
                <h4>View over the valid data </h4>
                <Table columns={columnsOptions}
                       dataSource={this.getValidRecordsData(validRecords)}
                       size="small"
                       scroll={{x: 1100}}
                       pagination={{pageSize: 5}}/>
                <Divider/>

                <h4>View over the invalid data </h4>
                <Table columns={columnsOptions}
                       dataSource={this.getValidRecordsData(invalidRecords)}
                       size="small"
                       scroll={{x: 1100}}
                       pagination={{pageSize: 5}}/>
            </div>
        )
    }
}

export default ConfirmStep;




