import React from 'react';
import {Redirect, Route} from 'react-router-dom';
import {checkAuthenticity} from "helpers";

export const PrivateRoute = ({ component: Component, ...rest }) => {
    return (
        <Route {...rest} render={props => (
            checkAuthenticity()
                ? <Component {...props} />
                : <Redirect to={{pathname: '/login', state: {from: props.location}}}/>
        )}/>
    )
};
