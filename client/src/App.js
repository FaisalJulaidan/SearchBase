import React, {Component, Suspense, lazy} from 'react';
import {Redirect, Route, Switch, withRouter} from 'react-router-dom';
import {connect} from 'react-redux';
import {history} from './helpers';
import {PrivateRoute} from './hoc';
import {destroyMessage} from './helpers/alert';
import SentryBoundary from "components/SentryBoundary/SentryBoundary";
import LoadingSpinner from "components/LoadingSpinner/LoadingSpinner";
import styles from "./components/LoadingSpinner/LoadingSpinner.module.less";


const Dashboard = lazy(() => import('./application/Dashboard/Dashboard'));
const Login = lazy(() => import('./application/Login/Login'));
const Signup = lazy(() => import('./application/Signup/Signup'));
const ForgetPassword = lazy(() => import('./application/ForgetPassword/ForgetPassword'));
const NewResetPassword = lazy(() => import('./application/ForgetPassword/NewResetPassword/NewResetPassword'));
const AppointmentsPicker = lazy(() => import('./application/AppointmentsPicker/AppointmentsPicker'));


class App extends Component {
    constructor(props) {
        super(props);
        // Clear recent notifications boxes when route changes
        history.listen(() => destroyMessage());
    }

    render() {
        return (
            <SentryBoundary>
                <Suspense fallback={<div className={styles.Loader}> Loading...</div>}>
                    <Switch>
                        {/* <Route exact path="/" component={Home} /> */}
                        <Route path="/login" component={Login}/>
                        <Route path="/signup" component={Signup}/>
                        <Route path="/forget_password" component={ForgetPassword}/>
                        <Route path="/reset_password/" component={NewResetPassword}/>
                        <Route path="/appointmentspicker/" component={AppointmentsPicker}/>
                        <PrivateRoute path="/dashboard" component={Dashboard}/>
                        <Redirect to={{pathname: '/dashboard'}}/>
                    </Switch>
                </Suspense>
            </SentryBoundary>
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
