import React from 'react'
import connect from "react-redux/es/connect/connect";
import styles from "../../Assistants.module.less";
import {Button, message} from "antd";
import Header from "./Header/Header";
import SolutionsDisplay from "./SolutionsDisplay/SolutionsDisplay";
import SolutionsSettings from "./SolutionsSettings/SolutionsSettings";
import {solutionsActions} from "../../../../../store/actions";
import Groups from "../Flow/Groups/Groups";

class Solutions extends React.Component{
    state = {
        currentSolution: {blocks: []},
        databaseConnectionTypes: ["Upload Export File"],
        databaseTypes: ["RDB XML File Export"]
    };

    componentDidMount() {
        console.log("MOUNTED PROPS: ", this.props);
        const {assistant} = this.props.location.state;
        this.props.dispatch(solutionsActions.getSolutions(assistant.ID))
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.solutions !== this.props.solutions) {
            console.log("SOLUTIONS RECEIVED");
            nextProps.solutionsData.map((solution) => {
                if (solution.id === this.state.currentSolution.id)
                    this.setState({currentSolution: solution})
            })
        }
    }

    selectSolution = (currentSolution) => this.setState({currentSolution});


    // GROUPS
    addSolution = (newSolution) => {
        // const {assistant} = this.props.location.state;
        // this.props.dispatch(flowActions.addSolutionRequest({ID: assistant.ID, newSolution: newSolution}));
        // message.loading(`Adding ${newSolution.name} group`, 0);
    };

    editSolution = (editedSolution) => {
        // const {assistant} = this.props.location.state;
        // this.props.dispatch(flowActions.editSolutionRequest({ID: assistant.ID, editedSolution: editedSolution}));
        // message.loading(`Editing ${editedSolution.name} group`, 0);
    };

    deleteSolution = (deletedSolution) => {
        // const {assistant} = this.props.location.state;
        // this.props.dispatch(flowActions.deleteSolutionRequest({ID: assistant.ID, deletedSolution: deletedSolution}));
        // message.loading(`Deleting ${deletedSolution.name} group`, 0);
    };

    componentDidUpdate(prevProps) {

        // if (!this.props.isAddingSolution && prevProps.addSuccessMsg !== this.props.addSuccessMsg) {
        //     message.destroy();
        //     message.success(this.props.addSuccessMsg);
        // }
        //
        // if (!this.props.isEditingSolution && prevProps.editSuccessMsg !== this.props.editSuccessMsg) {
        //     message.destroy();
        //     message.success(this.props.editSuccessMsg);
        // }
        //
        // if (!this.props.isDeletingSolution && prevProps.deleteSuccessMsg !== this.props.deleteSuccessMsg) {
        //     message.destroy();
        //     message.success(this.props.deleteSuccessMsg);
        // }
    }



    render(){
        console.log("PROPS: ", this.props);


        return (
             <div style={{height: '100%'}}>
                <div style={{padding: '0 5px'}}>
                    <div style={{width: '100%', height: 56, marginBottom: 10}}>
                        <Header display={"Solutions"}/>
                    </div>
                </div>

                <div style={{height: 'calc(100% - 66px)', width: '100%', display: 'flex'}}>
                    <div style={{margin: 5, width: '30%'}}>

                        <SolutionsDisplay selectSolution={this.selectSolution}
                                isLoading={this.props.isLoading}
                                solutionsData={this.props.solutionsData}
                                addGroup={this.addGroup}
                                editGroup={this.editGroup}
                                deleteGroup={this.deleteGroup}/>

                    </div>

                    <div style={{margin: 5, width: '70%'}}>

                        {/*<SolutionsSettings />*/}

                    </div>
                </div>
            </div>
        )
    }
}

function mapStateToProps(state) {
    console.log("PROPS STATE: ", state);
    return {
        solutionsData: state.solutions.solutionsData,
        isLoading: state.solutions.isLoading,
        errorMsg: state.solutions.errorMsg,
    };
}

export default connect(mapStateToProps)(Solutions)