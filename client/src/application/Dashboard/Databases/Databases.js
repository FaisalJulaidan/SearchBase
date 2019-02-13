import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Menu} from 'antd';

import styles from "./Databases.module.less"
import NewDatabaseModal from "./NewDatabaseModal/NewDatabaseModal";
import Header from "../../../components/Header/Header";
import {http} from "../../../helpers";
import {databaseActions} from "../../../store/actions";


class Databases extends Component {
    state = {
        visible: true,
    };

    componentWillMount() {
        http.get(`/databases/options`)
            .then(res => this.setState({databaseOptions: res.data.data}));

        this.props.dispatch(databaseActions.getDatabasesList());
    }


    showModal = () => this.setState({visible: true});
    hideModal = () => this.setState({visible: false});


    uploadDatabase = newDatabase => this.props.dispatch(databaseActions.uploadDatabase({newDatabase: newDatabase}));

    //
    // editGroup = (editedGroup) => {
    //     const {assistant} = this.props.location.state;
    //     this.props.dispatch(flowActions.editGroupRequest({assistantID: assistant.ID, editedGroup: editedGroup}));
    // };
    //
    // deleteGroup = (deletedGroup) => {
    //     const {assistant} = this.props.location.state;
    //     this.props.dispatch(flowActions.deleteGroupRequest({assistantID: assistant.ID, deletedGroup: deletedGroup}));
    //     this.setState({currentGroup: {blocks: []}});
    // };

    render() {
        return (
            <div style={{height: '100%'}}>
                <Header display={'Databases'} showBackButton={false}
                        button={{icon: "plus", onClick: this.showModal, text: 'Add Database'}}/>

                <div className={styles.Panel_Body_Only}>
                    <div style={{margin: '0 5px 0 0', width: '30%'}}>
                        <div className={styles.Panel}>

                            <div className={styles.Panel_Header} style={{position: "inherit"}}>
                                <h3>Databases List</h3>
                            </div>
                            <div className={styles.Panel_Body}>
                                <Menu mode="inline">
                                    {
                                        this.props.databasesList.map((database, index) =>
                                            <Menu.Item key={index}>{database.Name}</Menu.Item>)
                                    }
                                </Menu>
                            </div>
                        </div>

                    </div>

                    <div style={{margin: '0 0 0 5px', width: '70%'}}>
                        <div className={styles.Panel}>
                            <div className={styles.Panel_Header} style={{position: "inherit"}}>
                                <h3>Databases Information</h3>
                            </div>

                            <div className={styles.Panel_Body}>
                                hello world
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
        databasesList: state.database.databasesList
    };
}

export default connect(mapStateToProps)(Databases);
