import React, { Component, lazy, Suspense } from 'react';
import { Route, Switch, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import { PrivateRoute } from './hoc';
import SentryBoundary from 'components/SentryBoundary/SentryBoundary';
import styles from './components/LoadingSpinner/LoadingSpinner.module.less';

const Home = lazy(() => import('./application/Home/Home'));
const Dashboard = lazy(() => import('./application/Dashboard/Dashboard'));
const ForgetPassword = lazy(() => import('./application/ForgetPassword/ForgetPassword'));
const NewResetPassword = lazy(() => import('./application/ForgetPassword/NewResetPassword/NewResetPassword'));
const AppointmentsPicker = lazy(() => import('./application/AppointmentsPicker/AppointmentsPicker'));
const AccountVerification = lazy(() => import('./application/AccountVerification/AccountVerification'));
const ChatbotDirectLink = lazy(() => import('./application/ChatbotDirectLink/ChatbotDirectLink'));
const AppointmentStatus = lazy(() => import('./application/Public/AppointmentStatus/AppointmentStatus'));


class App extends Component {
    constructor(props) {
        super(props);
        // Build Client
        // Clear recent notifications boxes when route change
        // history.listen(() => destroyMessage());
    }


    render() {
        return (
            <SentryBoundary>
                <Suspense fallback={<div className={styles.Loader}> Loading...</div>}>
                    <Switch>
                        <Route path="/forget_password" component={ForgetPassword}/>
                        <Route path="/reset_password/" component={NewResetPassword}/>
                        <Route path="/verify_account/" component={AccountVerification}/>
                        <Route path="/appointments_picker/" component={AppointmentsPicker}/>
                        <Route path="/appointment_status/" component={AppointmentStatus}/>
                        <Route path="/chatbot_direct_link/" component={ChatbotDirectLink}/>
                        <PrivateRoute path="/dashboard" component={Dashboard}/>
                        <Route path="/" component={Home}/>
                         {/*<Redirect to={{pathname: '/'}}/> */}
                    </Switch>
                </Suspense>
            </SentryBoundary>
        );
    }
}

const mapStateToProps = (state) => {
    const { alert } = state;
    return {
        alert
    };
};
export default withRouter(connect(mapStateToProps)(App));
