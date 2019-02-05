import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Menu} from 'antd';

import styles from "./Databases.module.less"
import NewDatabaseModal from "./NewDataBaseModal/NewDatabaseModal";
import Header from "../../../components/Header/Header";
import {http} from "../../../helpers";

class Databases extends Component {
    state = {
        visible: true,
    };

    componentDidUpdate(prevProps) {

    }

    componentWillMount() {
        http.get(`/databases/options`)
            .then(res => this.setState({databaseOptions: res.data.data}))
    }


    showModal = () => this.setState({visible: true});
    hideModal = () => this.setState({visible: false});


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
                                    <Menu.Item key="9">Database 1</Menu.Item>
                                    <Menu.Item key="10">Database 2</Menu.Item>
                                    <Menu.Item key="11">Database 3</Menu.Item>
                                    <Menu.Item key="12">Database 4</Menu.Item>
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
                                  hideModal={this.hideModal}/>

            </div>
        );
    }
}

function mapStateToProps(state) {
    return {

    };
}

export default connect(mapStateToProps)(Databases);
