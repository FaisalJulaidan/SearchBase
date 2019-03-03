import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import {checkAuthenticity} from  '../helpers'

export const PrivateRoute = ({ component: Component, ...rest }) => {
    console.log("Check Authenticity", checkAuthenticity());
    return (
        <Route {...rest} render={props => (
            checkAuthenticity()
                ? <Component {...props} />
                : <Redirect to={{pathname: '/login', state: {from: props.location}}}/>
        )}/>
    )
}