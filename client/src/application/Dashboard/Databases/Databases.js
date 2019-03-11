import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Menu, Spin, Button, Modal} from 'antd';

import styles from "./Databases.module.less"
import NewDatabaseModal from "./NewDatabaseModal/NewDatabaseModal";
import Header from "../../../components/Header/Header";
import {databaseActions} from "../../../store/actions";

import DatabaseInfo from "./DatabaseInfo/DatabaseInfo"
import DatabaseDetailsModal from "./DatabaseDetailsModal/DatabaseDetailsModal"

const confirm = Modal.confirm;

class Databases extends Component {

    state = {
        visible: false,
        dbDetailsVisible: false
    };


    componentWillMount() {
        this.props.dispatch(databaseActions.getDatabasesList());
        console.log('DFGDFGDFGDGDFGDFGSDFGSWETHWRTHERTH');
    }


    showModal = () => this.setState({visible: true});
    hideModal = () => this.setState({visible: false});

    showDBDetails = () => this.setState({dbDetailsVisible: true});
    hideDBDetails = () => this.setState({dbDetailsVisible: false});

    updateDatabase = (updatedDatabase, databaseID) => {
        this.props.dispatch(databaseActions.updateDatabase(updatedDatabase, databaseID));
    };
    deleteDatabase = deletedDatabase => {
        confirm({
            title: `Delete database confirmation`,
            content: `If you click OK, this database will be deleted with its content forever`,
            onOk: () => {
                this.props.dispatch(databaseActions.deleteDatabase(deletedDatabase.databaseInfo.ID));
            }
        });
    };

    isDatabaseNameValid = (name) => {
        return !(this.props.databasesList.findIndex(db => db.Name === name) >= 0)
    };

    uploadDatabase = newDatabase => this.props.dispatch(databaseActions.uploadDatabase({newDatabase: newDatabase}));
    showDatabaseInfo = (databaseID) => this.props.dispatch(databaseActions.fetchDatabase(databaseID));


    componentWillUnmount() {
        this.props.dispatch(databaseActions.resetFetchedDatabase())
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
                            <div className={styles.Panel_Header_With_Button}>
                                <div>
                                    <h3>Databases Information</h3>
                                </div>
                                <div>
                                    <Button className={styles.Panel_Header_Button}
                                            disabled={!(!!this.props.fetchedDatabase?.databaseContent?.length)}
                                            type="primary" icon="info"
                                            onClick={this.showDBDetails}>
                                        Details
                                    </Button>
                                    <Button className={styles.Panel_Header_Button} type="danger" icon="delete"
                                            disabled={!(!!this.props.fetchedDatabase?.databaseContent?.length)}
                                            onClick={() => this.deleteDatabase(this.props.fetchedDatabase)}>
                                        Delete Database
                                    </Button>
                                </div>
                            </div>


                            <div className={styles.Panel_Body} style={{padding: 0}}>
                                {
                                    (
                                        (!!this.props.fetchedDatabase?.databaseContent?.length)
                                        &&
                                        (!!this.props.options.databases)
                                    ) ?
                                        <DatabaseInfo databaseOptions={this.props.options.databases}
                                                      databaseInfo={this.props.fetchedDatabase.databaseInfo}
                                                      data={this.getRecordsData(this.props.fetchedDatabase.databaseContent)}/>
                                        :
                                        <Spin spinning={this.props.isLoadingDatabase}>
                                            <div>
                                                <img
                                                    src="https://42f2671d685f51e10fc6-b9fcecea3e50b3b59bdc28dead054ebc.ssl.cf5.rackcdn.com/illustrations/following_q0cr.svg"
                                                    width={"50%"}
                                                    style={{
                                                        display: "block",
                                                        marginTop:20,
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
                            </div>
                        </div>
                    </div>
                </div>

                <NewDatabaseModal visible={this.state.visible}
                                  databaseOptions={this.props.options?.databases}
                                  uploadDatabase={this.uploadDatabase}
                                  isDatabaseNameValid={this.isDatabaseNameValid}
                                  hideModal={this.hideModal}/>


                <DatabaseDetailsModal visible={this.state.dbDetailsVisible}
                                      databaseOptions={this.props.options?.databases}
                                      databaseInfo={this.props.fetchedDatabase?.databaseInfo}
                                      hideModal={this.hideDBDetails}
                                      isDatabaseNameValid={this.isDatabaseNameValid}
                                      updateDatabase={this.updateDatabase}
                />


            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        databasesList: state.database.databasesList,
        fetchedDatabase: state.database.fetchedDatabase,
        isLoadingDatabase: state.database.isLoading,

        options: state.options.options,
    };
}

export default connect(mapStateToProps)(Databases);
