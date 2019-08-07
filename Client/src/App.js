import React, { Component, lazy, Suspense } from 'react';
import { Redirect, Route, Switch, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import { PrivateRoute } from './hoc';
import SentryBoundary from 'components/SentryBoundary/SentryBoundary';
import styles from './components/LoadingSpinner/LoadingSpinner.module.less';

import { TimezoneContext, getTimezone } from 'contexts/timezone';


const Dashboard = lazy(() => import('./application/Dashboard/Dashboard'));
const Login = lazy(() => import('./application/Login/Login'));
const Signup = lazy(() => import('./application/Signup/Signup'));
const ForgetPassword = lazy(() => import('./application/ForgetPassword/ForgetPassword'));
const NewResetPassword = lazy(() => import('./application/ForgetPassword/NewResetPassword/NewResetPassword'));
const AppointmentsPicker = lazy(() => import('./application/AppointmentsPicker/AppointmentsPicker'));
const AccountVerification = lazy(() => import('./application/AccountVerification/AccountVerification'));
const ChatbotDirectLink = lazy(() => import('./application/ChatbotDirectLink/ChatbotDirectLink'));
const AppointmentStatus = lazy(() => import('./application/Public/AppointmentStatus/AppointmentStatus'));


class App extends Component {
    constructor(props) {
        super(props);
        // Clear recent notifications boxes when route changes
        // history.listen(() => destroyMessage());
    }

    // setTimezone = async () => {
    //     let tz = await getTimezone();
    //     this.setState({ timezone: tz });
    //     this.pollTimezone();
    // };
    //
    // pollTimezone = () => {
    //     setInterval(async () => {
    //         let tz = await getTimezone();
    //         if (tz !== this.state.timezone) {
    //             this.setState({ timezone: tz });
    //         }
    //     }, 5000);
    // };
    //
    // componentDidMount() {
    //     this.setTimezone();
    // }

    state = {
        timezone: null
    };

    render() {
        return (
            <SentryBoundary>
                <Suspense fallback={<div className={styles.Loader}> Loading...</div>}>
                    <TimezoneContext.Provider value={this.state.timezone}>
                        <Switch>
                            {/* <Route exact path="/" component={Home} /> */}
                            <Route path="/login" component={Login}/>
                            <Route path="/signup" component={Signup}/>
                            <Route path="/forget_password" component={ForgetPassword}/>
                            <Route path="/reset_password/" component={NewResetPassword}/>
                            <Route path="/verify_account/" component={AccountVerification}/>
                            <Route path="/appointments_picker/" component={AppointmentsPicker}/>
                            <Route path="/appointment_status/" component={AppointmentStatus}/>
                            <Route path="/chatbot_direct_link/" component={ChatbotDirectLink}/>
                            <PrivateRoute path="/dashboard" component={Dashboard}/>
                            <Redirect to={{ pathname: '/dashboard' }}/>
                        </Switch>
                    </TimezoneContext.Provider>
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
