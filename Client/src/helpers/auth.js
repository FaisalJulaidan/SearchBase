import {store} from '../store/store'

export const authHeader = () => {
    // return authorization header with jwt token
    let token = localStorage.getItem('token');
    let refresh = localStorage.getItem('refresh');
    if (!token || !refresh) {return null}
    return {'Authorization': 'Bearer ' + token};
};


export const getUser = () => {
    // return user from local storage
    let user = JSON.parse(localStorage.getItem('user'));
    if(!user){return null;}
    return user;
};

export const getTimezone = () => {
    // return user from local storage
    let timezone = localStorage.getItem('timezone');
    if(!timezone){return null;}
    return timezone;
};

export const getRole = () => {
    // return role from local storage
    let role = JSON.parse(localStorage.getItem('role'));
    console.log('ROLE IS: ' + role);
    if(!role){return null;}
    return role;
};

export const getCompany = () => {
    // return plan from local storage
    let company = JSON.parse(localStorage.getItem('company'));
    if(!company){return null;}
    return company;
};

// Update username in localStorage
// Faisal small brain
export const updateUsername = (firstname, surname) => {
    // get user from localStorage
    let user = JSON.parse(localStorage.getItem('user'));
    if(!user){return null;}
    // update username and reset localStorage
    user.username = firstname + ' ' + surname;
    localStorage.setItem("user", JSON.stringify(user));
};

export const updateTimezone = (timezone) => {
    if(!timezone) return
    localStorage.setItem("timezone", timezone);
}



export const checkAuthenticity = () => {
    return (getUser() && getRole() && authHeader());
};

