import React from 'react';
import {Redirect, Route} from 'react-router-dom';

export const AuthorisedRoute = ({component: Component, permission: permission, ...rest}) => {
    return (
        <Route {...rest} render={props => (
            permission
                ? <Component {...props} />
                : <Redirect to={{pathname: '/dashboard', state: {from: props.location}}}/>
        )}/>
    )
};