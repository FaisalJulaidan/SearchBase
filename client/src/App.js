import React, {Component} from 'react';
import { Switch, Route, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import {history} from './helpers';
import './App.css';

import {PrivateRoute} from './hoc';
import Dashboard from "./containers/Dashboard/Dashboard";
import Login from './containers/Login/Login'

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
                <Route path="/login" component={Login} />
                <PrivateRoute path="/dashboard" component={Dashboard} />         
            </Switch>
        );
    }
}
    
const mapStateToProps = (state) => {
    const { alert } = state;
    return {
        alert
    };
}
export default withRouter(connect(mapStateToProps)(App));
