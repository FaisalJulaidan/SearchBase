import React, {Component} from "react";
import * as Sentry from '@sentry/browser';
import {connect} from 'react-redux';
import styles from './SentryBoundary.module.less';
import {getLink} from "helpers";
import {Button} from 'antd';

if (!(process.env.NODE_ENV === 'development'))
    Sentry.init({dsn: "https://12d2940f9cae4c8bb456358a2d550217@sentry.io/1436966"});

class SentryBoundary extends Component {

    constructor(props) {
        super(props);
        this.state = {error: null};
    }

    componentDidCatch(error, errorInfo) {
        this.setState({error});
        Sentry.withScope(scope => {
            scope.setExtras({
                errorInfo,
                debuggingState: this.props.debuggingState
            });
            const eventId = Sentry.captureException(error);
            this.setState({eventId})
        });
    }

    render() {
        if (this.state.error) {
            return (
                <div className={styles.Container}>
                    <div className={styles.NotFound}>
                        <div className={styles.NotFound404}>
                            <img src={"/images/error.svg"} alt="" height={'100%'}/>
                        </div>
                        <h1>404</h1>
                        <h2>We're sorry - something's gone wrong.</h2>
                        <p>Our team has been notified</p>

                        <br/>

                        <Button onClick={() => Sentry.showReportDialog({eventId: this.state.eventId})}
                                type={'primary'} style={{marginRight: 5}}>
                            Report Feedback
                        </Button>
                        <Button onClick={() => window.location.reload()} type={'default'}>Refresh Page</Button>
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

