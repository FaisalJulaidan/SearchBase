import React, {Component} from 'react';
import {Switch, Route, withRouter, Redirect} from 'react-router-dom';
import {connect} from 'react-redux';
import {history} from './helpers';
import './App.css';

import {PrivateRoute} from './hoc';
import Dashboard from "./components/Dashboard/Dashboard";
import Login from './components/Login/Login'

class App extends Component {
    constructor(props) {
        super(props);
        history.listen((location, action) => {
            console.log(`The current URL is ${location.pathname}${location.search}${location.hash}`)
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
