import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Menu, Table, Spin} from 'antd';

import styles from "./Databases.module.less"
import NewDatabaseModal from "./NewDatabaseModal/NewDatabaseModal";
import Header from "../../../components/Header/Header";
import {http} from "../../../helpers";
import {databaseActions} from "../../../store/actions";
import {ColumnsOptions} from "./NewDatabaseModal/ColumnsOptions";


class Databases extends Component {
    state = {
        visible: false,
    };

    componentWillMount() {
        http.get(`/databases/options`)
            .then(res => this.setState({databaseOptions: res.data.data}));

        this.props.dispatch(databaseActions.getDatabasesList());
    }


    showModal = () => this.setState({visible: true});
    hideModal = () => this.setState({visible: false});


    uploadDatabase = newDatabase => this.props.dispatch(databaseActions.uploadDatabase({newDatabase: newDatabase}));
    showDatabaseInfo = (databaseID) => this.props.dispatch(databaseActions.fetchDatabase(databaseID));


    componentWillUnmount() {
        this.props.dispatch(databaseActions.resetFetchedDtabase())
    }

    getRecordsData = records => {
        let x = [];
        for (const record of records) {
            let renderedRecord = {};
            for (const key of Object.keys(record))
                if (key !== 'DatabaseID')
                    renderedRecord[key] = record[key];

            x.push(renderedRecord);
        }
        return x;
    };

    render() {
        return (
            <div style={{height: '100%'}}>
                <Header display={'Databases'} showBackButton={false}
                        button={{icon: "plus", onClick: this.showModal, text: 'Add Database'}}/>

                <div className={styles.Panel_Body_Only}>
                    <div style={{margin: '0 5px 0 0', width: '20%'}}>
                        <div className={styles.Panel}>

                            <div className={styles.Panel_Header} style={{position: "inherit"}}>
                                <h3>Databases List</h3>
                            </div>
                            <div className={styles.Panel_Body}>
                                <Menu mode="inline">
                                    {
                                        this.props.databasesList.map((database, index) =>
                                            <Menu.Item key={index}
                                                       onClick={() => this.showDatabaseInfo(database.ID)}>{database.Name}</Menu.Item>)
                                    }
                                </Menu>
                            </div>
                        </div>

                    </div>

                    <div style={{margin: '0 0 0 5px', width: '80%'}}>
                        <div className={styles.Panel}>
                            <div className={styles.Panel_Header} style={{position: "inherit"}}>
                                <h3>Databases Information</h3>
                            </div>

                            <div className={styles.Panel_Body}>

                                {
                                    !!this.props.fetchedDatabase.databaseContent?.length ?
                                        <Table
                                            style={{height: '100%', width: 'auto'}}
                                            size={'small'}
                                            bordered
                                            columns={ColumnsOptions(this.props.fetchedDatabase.databaseContent[0], 'db')}
                                            dataSource={this.getRecordsData(this.props.fetchedDatabase.databaseContent)}
                                            rowKey={'ID'}
                                            pagination={{pageSize: 11}} scroll={{x: 3200}}/>
                                        :
                                        <Spin/>
                                }


                                {/*<pre>{*/}
                                {/*JSON.stringify(this.props.fetchedDatabase, null, 2)*/}
                                {/*}</pre>*/}
                            </div>
                        </div>
                    </div>
                </div>

                <NewDatabaseModal visible={this.state.visible}
                                  databaseOptions={this.state.databaseOptions}
                                  uploadDatabase={this.uploadDatabase}
                                  hideModal={this.hideModal}/>

            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        databasesList: state.database.databasesList,
        fetchedDatabase: state.database.fetchedDatabase
    };
}

export default connect(mapStateToProps)(Databases);
