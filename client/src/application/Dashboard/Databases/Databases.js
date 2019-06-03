import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Button, Menu, Modal, Icon, Typography} from 'antd';
import styles from "./Databases.module.less"

import NoHeaderPanel from 'components/NoHeaderPanel/NoHeaderPanel'
import UploadModal from "./UploadModal/UploadModal";
import {databaseActions} from "store/actions";
import CreateNewBox from "components/CreateNewBox/CreateNewBox";
import ViewBox from "components/ViewBox/ViewBox";
import EditModal from "./EditModal/EditModal"
import {DatabaseIcon} from "components/SVGs";
import {history} from "helpers";

import {getLink} from "helpers";

const {Title, Paragraph} = Typography;
const confirm = Modal.confirm;



class Databases extends Component {

    state = {
        uploadModalVisible: false,
        editModalVisible: false,
        databaseToEdit: null
    };


    componentWillMount() {
        this.props.dispatch(databaseActions.getDatabasesList());
    }


    showUploadModal = () => this.setState({uploadModalVisible: true});
    hideUploadModal = () => this.setState({uploadModalVisible: false});

    showEditModal = (database) => this.setState({editModalVisible: true, databaseToEdit: database});
    hideEditModal = () => this.setState({editModalVisible: false})

    updateDatabase = (updatedDatabase, databaseID) => {
        this.props.dispatch(databaseActions.updateDatabase(updatedDatabase, databaseID));
    };

    deleteDatabase = databaseID => {
        confirm({
            title: `Delete database confirmation`,
            content: `If you click OK, this database will be deleted with its content forever`,
            onOk: () => {
                this.props.dispatch(databaseActions.deleteDatabase(databaseID));
            }
        });
    };

    uploadDatabase = newDatabase => {
        this.props.dispatch(databaseActions.uploadDatabase({newDatabase: newDatabase}));
    };

    isDatabaseNameValid = (name) => {
        return !(this.props.databasesList.findIndex(db => db.Name.toLowerCase() === name.toLowerCase()) >= 0)
    };

    optionsMenuClickHandler = (e, database) => {
        if (e.key === 'edit')
            this.showEditModal(database);
        if (e.key === 'delete')
            this.deleteDatabase(database.ID)
    };

    // it must be an array of Menu.Item. ViewBox expect that in its options Menu
    optionsMenuItems = [
            <Menu.Item style={{padding:10, paddingRight: 30}} key="edit">
                <Icon type="edit" theme="twoTone" twoToneColor="#595959" style={{marginRight: 5}}/>
                Edit
            </Menu.Item>,
            <Menu.Item style={{padding:10, paddingRight: 30}} key="delete">
                <Icon type="delete" theme="twoTone" twoToneColor="#f50808" />
                Delete
            </Menu.Item>
    ];


    render() {
        return (

            <>
                <NoHeaderPanel>
                    <div className={styles.Title}>
                        <div className={styles.Details}>
                            <Title>Database</Title>
                            <Paragraph type="secondary">
                                Upload your database to empower your chatbot for candidates and jobs scanning
                            </Paragraph>
                        </div>
                    </div>

                    <div className={styles.Body}>
                        <CreateNewBox text={'Add Database'} onClick={this.showUploadModal}/>

                        {
                            this.props.databasesList.map(
                                (database, i) =>
                                    <ViewBox
                                        onClick={() => history.push(`/dashboard/databases/${database.ID}`)}
                                        optionsMenuItems={this.optionsMenuItems}
                                        optionsMenuClickHandler={(e)=>this.optionsMenuClickHandler(e, database)}
                                        key={i}
                                        title={database.Name}
                                        text={database.Type.name}
                                        icon={<DatabaseIcon/>}
                                        iconWidth={60} iconHeight={60} iconTop={188} iconRight={15}
                                    />
                            )
                        }
                    </div>
                </NoHeaderPanel>

                <UploadModal visible={this.state.uploadModalVisible}
                             databaseOptions={this.props.options?.databases}
                             uploadDatabase={this.uploadDatabase}
                             isDatabaseNameValid={this.isDatabaseNameValid}
                             hideModal={this.hideUploadModal}
                />


                <EditModal visible={this.state.editModalVisible}
                    databaseOptions={this.props.options?.databases}
                    database={this.state.databaseToEdit}
                    hideModal={this.hideEditModal}
                    isDatabaseNameValid={this.isDatabaseNameValid}
                    updateDatabase={this.updateDatabase}
                />

            </>

        );
    }
}

function mapStateToProps(state) {
    return {
        databasesList: state.database.databasesList,
        options: state.options.options,
    };
}

export default connect(mapStateToProps)(Databases);
