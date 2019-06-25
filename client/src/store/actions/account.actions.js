import * as actionTypes from './actionTypes';

const getAccount = () => {
    return {
        type: actionTypes.GET_ACCOUNT_REQUEST
    }
};

const getAccountSuccess = (account) => {
    return {
        type: actionTypes.GET_ACCOUNT_SUCCESS,
        account
    }
};

const getAccountFailure = (error) => {
    return {
        type: actionTypes.GET_ACCOUNT_FAILURE,
        error
    }
};

const saveProfileDetails = (profileData) => {
    return {
        type: actionTypes.SAVE_PROFILE_DETAILS_REQUEST,
        profileData
    }
};

const saveProfileDetailsSuccess = (successMsg) => {
    return {
        type: actionTypes.SAVE_PROFILE_DETAILS_SUCCESS,
        successMsg
    }
};

const saveProfileDetailsFailure = (error) => {
    return {
        type: actionTypes.SAVE_PROFILE_DETAILS_FAILURE,
        error
    }
};

const saveCompanyDetails = (companyData) => {
    return {
        type: actionTypes.SAVE_COMPANY_DETAILS_REQUEST,
        companyData
    }
};

const saveCompanyDetailsSuccess = (successMsg) => {
    return {
        type: actionTypes.SAVE_COMPANY_DETAILS_SUCCESS,
        successMsg
    }
};

const saveCompanyDetailsFailure = (error) => {
    return {
        type: actionTypes.SAVE_COMPANY_DETAILS_FAILURE,
        error
    }
};


const changePassword = (oldPassword, newPassword) => {
    return {
        type: actionTypes.CHANGE_PASS_REQUEST,
        oldPassword,
        newPassword
    }
};

const changePasswordSuccess = (successMsg) => {
    return {
        type: actionTypes.CHANGE_PASS_SUCCESS,
        successMsg
    }
};

const changePasswordFailure = (error) => {
    return {
        type: actionTypes.CHANGE_PASS_FAILURE,
        error
    }
};

const uploadLogo = (file) => {
    return {
        type: actionTypes.UPLOAD_LOGO_REQUEST,
        file
    };
};

const uploadLogoSuccess = (UpdatedLogoPath) => {
    return {
        type: actionTypes.UPLOAD_LOGO_SUCCESS,
        UpdatedLogoPath
    };
};

const uploadLogoFailure = (error) => {
    return {
        type: actionTypes.UPLOAD_LOGO_FAILURE,
        error
    };
};

const deleteLogo = () => {
    return {
        type: actionTypes.DELETE_LOGO_REQUEST,
    };
};

const deleteLogoSuccess = (msg) => {
    return {
        type: actionTypes.DELETE_LOGO_SUCCESS,
        msg
    };
};

const deleteLogoFailure = (error) => {
    return {
        type: actionTypes.DELETE_LOGO_FAILURE,
        error
    };
};

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