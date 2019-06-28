import * as actionTypes from './actionTypes';

const getAccount = () => ({
    type: actionTypes.GET_ACCOUNT_REQUEST
});

const getAccountSuccess = (account) => ({
    type: actionTypes.GET_ACCOUNT_SUCCESS,
    account
});

const getAccountFailure = (error) => ({
    type: actionTypes.GET_ACCOUNT_FAILURE,
    error
});

const saveProfileDetails = (profileData) => ({
    type: actionTypes.SAVE_PROFILE_DETAILS_REQUEST,
    profileData
});

const saveProfileDetailsSuccess = (successMsg) => ({
    type: actionTypes.SAVE_PROFILE_DETAILS_SUCCESS,
    successMsg
});

const saveProfileDetailsFailure = (error) => ({
    type: actionTypes.SAVE_PROFILE_DETAILS_FAILURE,
    error
});

const saveCompanyDetails = (companyData) => ({
    type: actionTypes.SAVE_COMPANY_DETAILS_REQUEST,
    companyData
});

const saveCompanyDetailsSuccess = (successMsg) => ({
    type: actionTypes.SAVE_COMPANY_DETAILS_SUCCESS,
    successMsg
});

const saveCompanyDetailsFailure = (error) => ({
    type: actionTypes.SAVE_COMPANY_DETAILS_FAILURE,
    error
});


const changePassword = (oldPassword, newPassword) => ({
    type: actionTypes.CHANGE_PASS_REQUEST,
    oldPassword,
    newPassword
});

const changePasswordSuccess = (successMsg) => ({
    type: actionTypes.CHANGE_PASS_SUCCESS,
    successMsg
});

const changePasswordFailure = (error) => ({
    type: actionTypes.CHANGE_PASS_FAILURE,
    error
});

const uploadLogo = (file) => ({
    type: actionTypes.UPLOAD_LOGO_REQUEST,
    file
});

const uploadLogoSuccess = (UpdatedLogoPath) => ({
    type: actionTypes.UPLOAD_LOGO_SUCCESS,
    UpdatedLogoPath
});

const uploadLogoFailure = (error) => ({
    type: actionTypes.UPLOAD_LOGO_FAILURE,
    error
});

const deleteLogo = () => ({
    type: actionTypes.DELETE_LOGO_REQUEST,
});

const deleteLogoSuccess = (msg) => ({
    type: actionTypes.DELETE_LOGO_SUCCESS,
    msg
});

const deleteLogoFailure = (error) => ({
    type: actionTypes.DELETE_LOGO_FAILURE,
    error
});

export const accountActions = {
    getAccount,
    getAccountSuccess,
    getAccountFailure,
    saveProfileDetails,
    saveProfileDetailsSuccess,
    saveProfileDetailsFailure,
    saveCompanyDetails,
    saveCompanyDetailsSuccess,
    saveCompanyDetailsFailure,

    changePassword,
    changePasswordSuccess,
    changePasswordFailure,

    uploadLogo,
    uploadLogoSuccess,
    uploadLogoFailure,

    deleteLogo,
    deleteLogoSuccess,
    deleteLogoFailure,
};
