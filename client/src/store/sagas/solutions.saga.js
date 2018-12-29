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
        yield put(solutionsActions.addSolutionSuccess(res.message));
        yield destroyMessage();
        yield alertSuccess('Solution Added', res.data.msg);
        return yield http.get(solutionsActions.getSolutions(action.assistantID))
    } catch (error) {
        console.log(error.response);
        yield alertError('Error in adding Solution', error.response.data.msg);
        return yield put(solutionsActions.addSolutionFailure(error.response.data));
    }

}

function* watchSolutionsRequests(){
    yield takeEvery(actionTypes.GET_SOLUTIONS_REQUEST, getSolutionsData)
}

function* watchAddSolutionRequests(){
    yield takeEvery(actionTypes.ADD_SOLUTION_REQUEST, addSolution)
}

export function* solutionsSaga() {
    yield all([
        watchSolutionsRequests(),
        watchAddSolutionRequests()
    ])
}