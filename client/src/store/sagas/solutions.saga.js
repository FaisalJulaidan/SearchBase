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
        yield put(solutionsActions.getSolutions(action.params.ID));
    } catch (error) {
        console.log(error.response);
        yield destroyMessage();
        yield alertError('Error in adding Solution', error.response.data.msg);
        yield put(solutionsActions.addSolutionFailure(error.response.data));
    }
}

function* editSolution(action) {
    try {
        loadingMessage('Editing Solution');
        const res = yield http.post(`/assistant/${action.params.ID}/solutionsData`, action.params.editedSolution);
        yield destroyMessage();
        yield alertSuccess('Solution Edited', res.data.msg);
        yield put(solutionsActions.editSolutionSuccess(res.message));
        yield put(solutionsActions.getSolutions(action.params.ID))
    } catch (error) {
        console.log(error.response);
        yield destroyMessage();
        yield alertError('Error in editing Solution', error.response.data.msg);
        yield put(solutionsActions.editSolutionFailure(error.response.data));
    }
}

function* updateSolutionInformationToDisplay(action) {
    try {
        loadingMessage('Editing Display Settings');
        const res = yield http.post(`/assistant/savedisplaytitles/${action.params.solutionID}`, action.params.information);
        yield destroyMessage();
        yield alertSuccess('Display Settings have been edited', res.data.msg);
        yield put(solutionsActions.updateSolutionInformationToDisplaySuccess(res.message));
    } catch (error) {
        console.log(error.response);
        yield alertError('Error in editing Display Settings', error.response.data.msg);
        yield put(solutionsActions.updateSolutionInformationToDisplayFailure(error.response.data));
    }
}

function* updateButtonLink(action) {
    try {
        loadingMessage('Updating Button Link');
        const res = yield http.post(`/assistant/savesolutionweblink/${action.params.solutionID}`, action.params.information);
        yield destroyMessage();
        yield alertSuccess('Button Link has been updated', res.data.msg);
        yield put(solutionsActions.updateButtonLinkSuccess(res.message));
    } catch (error) {
        console.log(error.response);
        yield alertError('Error in updating Button Link', error.response.data.msg);
        yield put(solutionsActions.updateButtonLinkFailure(error.response.data));
    }
}

function* sendSolutionAlerts(action) {
    try {
        loadingMessage('Sending Solution Alerts');
        const res = yield http.post(`/assistant/${action.params.assistantID}/sendsolutionalerts/${action.params.solutionID}`);
        yield destroyMessage();
        yield alertSuccess('Solution Alerts have been sent', res.data.msg);
        yield put(solutionsActions.sendSolutionAlertSuccess(res.message));
    } catch (error) {
        console.log(error.response);
        yield alertError('Error in sending Solution Alerts', error.response.data.msg);
        yield put(solutionsActions.sendSolutionAlertFailure(error.response.data));
    }
}

function* updateAutomaticSolutionsAlerts(action) {
    try {
        loadingMessage('Updating Automatic Solution Alerts');
        const res = yield http.post(`/assistant/automaticsolutionalerts/${action.params.solutionID}`, action.params.information);
        yield destroyMessage();
        yield alertSuccess('Automatic Solution Alerts have been updated', res.data.msg);
        yield put(solutionsActions.updateAutomaticSolutionsSuccess(res.message));
    } catch (error) {
        console.log(error.response);
        yield alertError('Error in updating Automatic Solution Alerts', error.response.data.msg);
        yield put(solutionsActions.updateAutomaticSolutionsFailure(error.response.data));
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

function* watchUpdateButtonLinkRequests(){
    yield takeEvery(actionTypes.UPDATE_BUTTON_LINK_REQUEST, updateButtonLink)
}

function* watchSendSolutionAlertsRequests(){
    yield takeEvery(actionTypes.SEND_SOLUTION_ALERT_REQUEST, sendSolutionAlerts)
}

function* watchUpdateAutomaticSolutionAlertsRequests(){
    yield takeEvery(actionTypes.UPDATE_AUTOMATIC_SOLUTION_ALERTS_REQUEST, updateAutomaticSolutionsAlerts)
}

export function* solutionsSaga() {
    yield all([
        watchSolutionsRequests(),
        watchAddSolutionRequests(),
        watchEditSolutionRequests(),
        watchUpdateSolutionInformationToDisplayRequests(),
        watchUpdateButtonLinkRequests(),
        watchSendSolutionAlertsRequests(),
        watchUpdateAutomaticSolutionAlertsRequests()
    ])
}