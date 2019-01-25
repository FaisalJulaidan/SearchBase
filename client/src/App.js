import React, {Component} from 'react';
import {Redirect, Route, Switch, withRouter} from 'react-router-dom';
import {connect} from 'react-redux';
import {history} from './helpers';
import {notification} from 'antd';

import {PrivateRoute} from './hoc';
import Dashboard from "./application/Dashboard/Dashboard";
import Login from './application/Login/Login'

class App extends Component {
    constructor(props) {
        super(props);
        history.listen((location, action) => {
            // Clear recent notifications boxes when route changes
            notification.destroy();
        });
    }

    render() {
        return (
            <Switch>
                {/* <Route exact path="/" component={Home} /> */}
                <Route path="/login" component={Login}/>
                <PrivateRoute path="/dashboard" component={Dashboard}/>
                <Redirect to={{pathname: '/dashboard'}}/>
            </Switch>
        );
    }
}

const mapStateToProps = (state) => {
    const {alert} = state;
    return {
        alert,
    };
};
export default withRouter(connect(mapStateToProps)(App));
