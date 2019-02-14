import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Menu, Table, Spin} from 'antd';

import styles from "./Databases.module.less"
import NewDatabaseModal from "./NewDatabaseModal/NewDatabaseModal";
import Header from "../../../components/Header/Header";
import {http} from "../../../helpers";
import {databaseActions} from "../../../store/actions";
import {ColumnsOptions} from "./NewDatabaseModal/ColumnsOptions";

import DatabaseInfo from "./DatabaseInfo/DatabaseInfo"

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

        if (records) {
            for (const record of records) {
                let renderedRecord = {};
                for (const key of Object.keys(record))
                    if (key !== 'DatabaseID')
                        renderedRecord[key] = record[key];

                x.push(renderedRecord);
            }
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

                            <div className={styles.Panel_Body} style={{padding: 0}}>

                                {/*{*/}
                                {/*!!this.props.fetchedDatabase.databaseContent?.length ?*/}
                                {/*<Table*/}
                                {/*style={{height: '100%', width: 'auto'}}*/}
                                {/*// size={'small'}*/}
                                {/*// bordered*/}
                                {/*columns={ColumnsOptions(this.props.fetchedDatabase.databaseContent[0], 'db')}*/}
                                {/*dataSource={this.getRecordsData(this.props.fetchedDatabase.databaseContent)}*/}
                                {/*rowKey={'ID'}*/}
                                {/*pagination={{pageSize: 11}} scroll={{x: 3200}}/>*/}
                                {/*:*/}
                                {/*<div>*/}
                                {/*<img*/}
                                {/*src="https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/following_q0cr.svg"*/}
                                {/*width={"50%"}*/}
                                {/*style={{*/}
                                {/*display: "block",*/}
                                {/*marginLeft: "auto",*/}
                                {/*marginRight: "auto",*/}
                                {/*}}*/}
                                {/*/>*/}
                                {/*<p style={{textAlign: 'center', marginTop: 5}}>*/}
                                {/*Select a database to show its data*/}
                                {/*</p>*/}
                                {/*</div>*/}

                                {/*}*/}


                                {
                                    !!this.props.fetchedDatabase.databaseContent?.length ?
                                        <DatabaseInfo
                                            data={this.getRecordsData(this.props.fetchedDatabase.databaseContent)}/>
                                        :
                                        <Spin spinning={this.props.isLoadingDatabase}>
                                            <div>
                                                <img
                                                    src="https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/following_q0cr.svg"
                                                    width={"50%"}
                                                    style={{
                                                        display: "block",
                                                        marginLeft: "auto",
                                                        marginRight: "auto",
                                                    }}
                                                />
                                                <p style={{textAlign: 'center', marginTop: 5}}>
                                                    Select a database to show its data
                                                </p>
                                            </div>
                                        </Spin>
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
        fetchedDatabase: state.database.fetchedDatabase,
        isLoadingDatabase: state.database.isLoading
    };
}

export default connect(mapStateToProps)(Databases);
