
export const authHeader = () => {
    // return authorization header with jwt token
    let token = localStorage.getItem('token');
    let refresh = localStorage.getItem('refresh');
    if (!token || !refresh) {return null}
    return {'Authorization': 'Bearer ' + token};
}


export const getUser = () => {
    // return user from local storage
    let user = JSON.parse(localStorage.getItem('user'));
    if(!user){return null;}
    return user;
}

export const checkAuthenticity = () => {
    return !(!getUser() || !authHeader());

}

