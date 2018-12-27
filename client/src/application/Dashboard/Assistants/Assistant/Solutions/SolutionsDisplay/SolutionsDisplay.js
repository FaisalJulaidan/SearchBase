import React from 'react';
import styles from "../Solutions.module.less";
import {Avatar, Button, List, Skeleton, Spin} from "antd";
import NewSolution from "./NewSolution/NewSolution";

class SolutionsDisplay extends React.Component{
    state = {
        newSolutionModal: false,
        editSolutionModal: false,
        selectedSolutionToEdit: {}
    };

    handleAddSolution = (newSolution) => {
        this.props.addSolution(newSolution);
        this.setState({newSolutionModal: false});
    };

    handleAddSolutionCancel = () => this.setState({newSolutionModal: false});

    showNewSolutionModal = () => this.setState({newSolutionModal: true});


    ////// EDIT GROUP
    handleEditSolution = (editedSolution) => {
        this.props.editSolution(editedSolution);
        this.setState({editSolutionModal: false, selectedSolutionToEdit: {}});
    };

    handleEditSolutionCancel = () => this.setState({editSolutionModal: false});

    showEditSolutionModal = (item) => this.setState({editSolutionModal: true, selectedSolutionToEdit: item});

    ////// DELETE GROUP
    handleDeleteSolution = (deletedSolution) => {
        this.props.deleteSolution(deletedSolution);
        this.setState({editSolutionModal: false, selectedSolutionToEdit: {}});
    };

    render (){
        console.log("SOLUTIONS DISPLAY PROPS ON RENDER: ", this.props);

        return(
            <div className={styles.Panel}>
                <div className={styles.Header} style={{}}>
                    <div>
                        <h3>Solutions List</h3>
                    </div>
                    <div>
                        <Button className={styles.PanelButton} type="primary" icon="plus"
                                onClick={this.showNewSolutionModal}>
                            Add Solution
                        </Button>

                        <NewSolution visible={this.state.newSolutionModal}
                                     handleCancel={this.handleAddSolutionCancel}
                                     handleSave={this.handleAddSolution}
                                     databaseFileTypes={this.props.databaseFileTypes}
                                     databaseCRMTypes={this.props.databaseCRMTypes}
                        />
                    </div>
                </div>


                <div className={styles.Body}>
                    {
                        this.props.isLoading ?
                            <Spin><Skeleton active={true}/></Spin>
                            :
                            <List
                                itemLayout="horizontal"
                                dataSource={this.props.solutionsData}
                                renderItem={item => (
                                    <List.Item
                                        actions={[<Button icon={'edit'}
                                                          onClick={() => this.showEditSolutionModal(item)}/>]}>
                                        <List.Item.Meta
                                            avatar={<Avatar icon="ordered-list"
                                                            style={{backgroundColor: '#9254de'}}/>}
                                            title={<a onClick={() => this.props.selectSolution(item)}>{item.Solution.Name}</a>}
                                            description={item.description}
                                        />
                                    </List.Item>
                                )}
                            />
                    }
                </div>

                {/*<EditSolution group={this.state.selectedSolutionToEdit}*/}
                           {/*visible={this.state.editSolutionModal}*/}
                           {/*handleCancel={this.handleEditSolutionCancel}*/}
                           {/*handleUpdate={this.handleEditSolution}*/}
                           {/*handleDelete={this.handleDeleteSolution}/>*/}
            </div>
        )
    }
}

export default SolutionsDisplay