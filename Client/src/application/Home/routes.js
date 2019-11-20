import React, {Component} from 'react'
import {Route, Switch} from 'react-router-dom'

import Home from './component/page/home/Home'
import Terms from "./component/page/terms/Terms";
import HowItWorks from "./component/page/how-it-works/HowItWorks";
import Policies from "./component/page/privacy/Policies";
import NotFound404 from "./component/page/not-found-404/NotFound404";
import OurTeam from "./component/page/our-team/OurTeam";
import ReleaseNote from "./component/page/release-note/ReleaseNote";
import Login from "./component/page/login/Login";
import Signup from "./component/page/signup/Signup";
import GDPR from "./component/page/gdpr/GDPR";
import GetStarted from "./component/page/get-started/GetStarted";
import SuccessfulLogin from "./component/util/SuccessfulLogin";
import Pricing from "./component/page/pricing/Pricing";
import Payment from "./component/page/payment/Payment";
import SuccessPayment from "./component/page/payment/success/SuccessPayment";
import ROI from "./component/page/roi/ROI";

class Routes extends Component {
    render() {
        return (
            <Switch>
                <Route path="/" exact component={Home}/>
                <Route path="/features" exact component={HowItWorks}/>
                <Route path="/how-it-works" exact component={HowItWorks}/>
                <Route path="/pricing" exact component={Pricing}/>
                <Route path="/roi" exact component={ROI}/>
                <Route path="/order-plan" exact component={Payment}/>
                <Route path="/success-payment" exact component={SuccessPayment}/>
                <Route path="/our-team" exact component={OurTeam}/>
                <Route path="/terms" exact component={Terms}/>
                <Route path="/privacy" exact component={Policies}/>
                <Route path="/gdpr" exact component={GDPR}/>
                <Route path="/release-notes" exact component={ReleaseNote}/>
                <Route path="/login" exact component={Login}/>
                <Route path="/signup" exact component={Signup}/>
                <Route path="/get-started" exact component={GetStarted}/>
                <Route path="/successful-login" exact component={SuccessfulLogin}/>
                <Route path="" exact component={NotFound404}/>
            </Switch>
        )
    }
}

export default Routes;
