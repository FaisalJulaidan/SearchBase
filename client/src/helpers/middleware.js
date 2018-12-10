import {checkAuthenticity} from './auth';
import {authActions} from "../store/actions";

export function authMiddleware() {
    return ({ dispatch, getState }) => next => (action) => {
        console.log('Inside Auth middleware')
        console.log(action);
        console.log(next);
        const {request} = action;

        if (!request) {
            return next(action);
        }

        const refresh = localStorage.getItem("refresh");
        if (!refresh) {
            dispatch(authActions.logout());
        }

        if (!checkAuthenticity) {
            dispatch(authActions.setToken(refresh));
        }
        // return request(tokens);
    };
}