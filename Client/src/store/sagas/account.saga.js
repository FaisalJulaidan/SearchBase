import { all, put, takeEvery, takeLatest } from 'redux-saga/effects';
import * as actionTypes from '../actions/actionTypes';
import { accountActions } from '../actions';
import {
    errorMessage,
    http,
    loadingMessage,
    successMessage,
    updateUsername,
    updateTimezone
} from 'helpers';

function* getAccountDetails() {
    try {
        const res = yield http.get(`/account`);
        const account = yield res.data?.data;

        // Update username in localStorage
        let file = account.company.StoredFile?.StoredFileInfo?.find(
            item => item.Key === 'Logo'
        );
        // console.log()
        account.company.LogoPath = file?.AbsFilePath || null;
        yield updateUsername(account.user.Firstname, account.user.Surname);
        yield updateTimezone(account.user.TimeZone);

        yield put(accountActions.getAccountSuccess(account));
    } catch (error) {
        console.log(error);
        const msg =
            error.response?.data?.msg || "Couldn't load account details";
        yield put(accountActions.getAccountFailure(msg));
        errorMessage(msg);
    }
}

function* saveProfileData({ profileData }) {
    try {
        loadingMessage('Saving profile...', 0);
        const res = yield http.post(`/profile`, profileData);
        yield put(accountActions.saveProfileDetailsSuccess(res.data.msg));
        yield put(accountActions.getAccount());
        successMessage('Profile saved');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't save profile";
        yield put(accountActions.saveProfileDetailsFailure(msg));
        errorMessage(msg);
    }
}

function* saveCompanyDetails({ companyData }) {
    try {
        loadingMessage('Saving company settings...', 0);
        const res = yield http.post(`/company`, companyData);
        yield put(accountActions.saveCompanyDetailsSuccess(res.data.msg));
        yield put(accountActions.getAccount());
        successMessage('Company settings saved');
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't save settings";
        yield put(accountActions.saveCompanyDetailsFailure(msg));
        errorMessage(msg);
    }
}

function* changePassword({ newPassword, oldPassword }) {
    try {
        loadingMessage('Updating passwords...', 0);
        const res = yield http.post(`/profile/password`, {
            newPassword,
            oldPassword
        });
        yield put(accountActions.changePasswordSuccess(res.data.msg));
        successMessage('Password updated');
    } catch (error) {
        console.log(error.response);
        const msg = error.response?.data?.msg || 'Old password is incorrect';
        yield put(accountActions.changePasswordFailure(msg));
        errorMessage(msg);
    }
}

function* uploadLogo({ file }) {
    try {
        loadingMessage('Uploading logo', 0);
        const res = yield http.post(`/company/logo`, file);
        yield successMessage('Logo uploaded');
        console.log(res.data.data);
        yield put(accountActions.uploadLogoSuccess(res.data?.data));
    } catch (error) {
        const msg = error.response?.data?.msg || "Couldn't upload logo";
        errorMessage(msg);
        yield put(accountActions.uploadLogoFailure(msg));
    }
}

function* deleteLogo() {
    try {
        loadingMessage('Deleting logo', 0);
        const res = yield http.delete(`/company/logo`);
        successMessage('Logo deleted');
        yield put(accountActions.deleteLogoSuccess());
    } catch (error) {
        const msg = error.response?.data?.msg || "Can't delete logo";
        errorMessage(msg);
        yield put(accountActions.deleteLogoFailure(msg));
    }
}

function* watchUploadLogo() {
    yield takeEvery(actionTypes.UPLOAD_LOGO_REQUEST, uploadLogo);
}

function* watchDeleteLogo() {
    yield takeEvery(actionTypes.DELETE_LOGO_REQUEST, deleteLogo);
}

function* watchAccountRequests() {
    yield takeLatest(actionTypes.GET_ACCOUNT_REQUEST, getAccountDetails);
}

function* watchProfileUpdates() {
    yield takeLatest(actionTypes.SAVE_PROFILE_DETAILS_REQUEST, saveProfileData);
}

function* watchCompanyDetailsUpdates() {
    yield takeLatest(
        actionTypes.SAVE_COMPANY_DETAILS_REQUEST,
        saveCompanyDetails
    );
}

function* watchChangePassword() {
    yield takeLatest(actionTypes.CHANGE_PASS_REQUEST, changePassword);
}

export function* accountSaga() {
    yield all([
        watchAccountRequests(),
        watchProfileUpdates(),
        watchCompanyDetailsUpdates(),
        watchChangePassword(),
        watchUploadLogo(),
        watchDeleteLogo()
    ]);
}
