import React from 'react';
import styles from "../Solutions.module.less";
import {Avatar, Button, List, Skeleton, Spin} from "antd";
import SolutionModal from "./SolutionModal/SolutionModal";

class SolutionsDisplay extends React.Component{
    state = {
        SolutionModal: false,
        editMode: false,
        selectedSolutionToEdit: {}
    };

    handleSolution = (Solution, edit) => {
        if(!edit){
            this.props.addSolution(Solution);
            this.setState({SolutionModal: false, editMode:false});
        } else {
            this.props.editSolution(Solution);
            this.setState({SolutionModal: false, editMode:false});
        }
    };

    handleSolutionCancel = () => this.setState({SolutionModal: false, editMode:false});

    showSolutionModal = () => this.setState({SolutionModal: true});

    selectSolution = (item) => {
        this.setState({selectedSolutionToEdit: item, editMode:true, SolutionModal:true});
    };

    // ////// DELETE GROUP
    // handleDeleteSolution = (deletedSolution) => {
    //     this.props.deleteSolution(deletedSolution);
    //     this.setState({editSolutionModal: false, selectedSolutionToEdit: {}});
    // };

    render (){
        return(
            <div className={styles.Panel}>
                <div className={styles.Panel_Header}>
                    <div>
                        <h3>Solutions List</h3>
                    </div>
                    <div>
                        <Button className={styles.Panel_Header_Button} type="primary" icon="plus"
                                onClick={this.showSolutionModal}>
                            Add Solution
                        </Button>
                    </div>
                </div>


                <div className={styles.Panel_Body}>
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
                                                          onClick={() => this.selectSolution(item)}/>]}>
                                        <List.Item.Meta
                                            avatar={<Avatar icon="database"
                                                            style={{backgroundColor: '#9254de'}}/>}
                                            title={<a onClick={() => this.props.selectSolution(item)}>{item.Solution.Name}</a>}
                                            description={item.description}
                                        />
                                    </List.Item>
                                )}
                            />
                    }
                </div>

                <SolutionModal visible={this.state.SolutionModal}
                                     handleCancel={this.handleSolutionCancel}
                                     handleSave={this.handleSolution}
                                     databaseFileTypes={this.props.databaseFileTypes}
                                     databaseCRMTypes={this.props.databaseCRMTypes}
                                     edit={this.state.editMode}
                                     solutionToEdit={this.state.editMode ? this.state.selectedSolutionToEdit : {}}
                        />
            </div>
        )
    }
}

export default SolutionsDisplay