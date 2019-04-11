import React, {Component} from "react";
import * as Sentry from '@sentry/browser';
import {connect} from 'react-redux';

Sentry.init({
    dsn: "https://12d2940f9cae4c8bb456358a2d550217@sentry.io/1436966"
});

class SentryBoundary extends Component {


    constructor(props) {
        super(props);
        this.state = {error: null};


        // should have been called before using it here
        // ideally before even rendering your react app
    }

    componentDidCatch(error, errorInfo) {
        this.setState({error});
        // Sentry.withScope(scope => {
        //     scope.setExtras({
        //         ...errorInfo,
        //         debuggingState: this.props.debuggingState
        //     });
        //     const eventId = Sentry.captureException(error);
        //     this.setState({eventId})
        // });
    }

    render() {
        if (this.state.error) {
            return (
                <div className="snap">
                    <img src={'https://wiggly-power.glitch.me/static/media/sentry-aw-snap.afe2fd59.svg'}/>
                    <div className="snap-message">
                        <p>We're sorry - something's gone wrong.</p>
                        <p>Our team has been notified</p>
                        <a onClick={() => Sentry.showReportDialog({eventId: this.state.eventId})}>Report feedback</a>

                    </div>

                </div>
            );
        } else {
            return this.props.children;
        }
    }
}

function mapStateToProps(state) {
    return {
        debuggingState: state
    };
}

export default connect(mapStateToProps)(SentryBoundary);

