import {put, takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes';
import {http} from "../../helpers";
import {solutionsActions} from "../actions";
import {alertError, alertSuccess, destroyMessage, loadingMessage} from "../../helpers/alert";


function* getSolutionsData({assistantID}) {
    try {
        const res = yield http.get(`/assistant/${assistantID}/solutionsData`);
        return yield put(solutionsActions.getSolutionsSuccess(res.data))
    } catch (error) {
        console.log(error);
        return yield put(solutionsActions.getSolutionsFailure(error.response.data));
    }

}

function* addSolution(action) {
    try {
        loadingMessage('Adding Solution');
        const res = yield http.put(`/assistant/${action.params.ID}/solutionsData`, action.params.newSolution);
        yield destroyMessage();
        yield alertSuccess('Solution Added', res.data.msg);
        yield put(solutionsActions.addSolutionSuccess(res.message));
        return yield http.get(solutionsActions.getSolutions(action.assistantID))
    } catch (error) {
        console.log(error.response);
        yield alertError('Error in adding Solution', error.response.data.msg);
        return yield put(solutionsActions.addSolutionFailure(error.response.data));
    }
}

function* editSolution(action) {
    try {
        loadingMessage('Editing Solution');
        const res = yield http.post(`/assistant/${action.params.ID}/solutionsData`, action.params.editedSolution);
        yield destroyMessage();
        yield alertSuccess('Solution Edited', res.data.msg);
        yield put(solutionsActions.editSolutionSuccess(res.message));
        return yield http.get(solutionsActions.getSolutions(action.assistantID))
    } catch (error) {
        console.log(error.response);
        yield alertError('Error in editing Solution', error.response.data.msg);
        return yield put(solutionsActions.editSolutionFailure(error.response.data));
    }
}

function* updateSolutionInformationToDisplay(action) {
    try {
        loadingMessage('Editing Solution Settings');
        const res = yield http.post(`/assistant/savedisplaytitles/${action.params.solutionID}`, action.params.information);
        yield destroyMessage();
        yield alertSuccess('Solution Settings Edited', res.data.msg);
        return yield put(solutionsActions.updateSolutionInformationToDisplaySuccess(res.message));
    } catch (error) {
        console.log(error.response);
        yield alertError('Error in editing Solution Settings', error.response.data.msg);
        return yield put(solutionsActions.updateSolutionInformationToDisplayFailure(error.response.data));
    }
}

function* watchSolutionsRequests(){
    yield takeEvery(actionTypes.GET_SOLUTIONS_REQUEST, getSolutionsData)
}

function* watchAddSolutionRequests(){
    yield takeEvery(actionTypes.ADD_SOLUTION_REQUEST, addSolution)
}

function* watchEditSolutionRequests(){
    yield takeEvery(actionTypes.EDIT_SOLUTION_REQUEST, editSolution)
}

function* watchUpdateSolutionInformationToDisplayRequests(){
    yield takeEvery(actionTypes.UPDATE_SOLUTION_INFORMATION_TO_DISPLAY_REQUEST, updateSolutionInformationToDisplay)
}

export function* solutionsSaga() {
    yield all([
        watchSolutionsRequests(),
        watchAddSolutionRequests(),
        watchEditSolutionRequests(),
        watchUpdateSolutionInformationToDisplayRequests()
    ])
}