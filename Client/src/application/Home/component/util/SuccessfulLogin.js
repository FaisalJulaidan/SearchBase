import React, {Component} from 'react';
import {history} from 'helpers';
import queryString from 'query-string';

class SuccessfulLogin extends Component {

    componentDidMount() {
        if (queryString.parse(this.props.location.search)?.prevPath)
            history.push(queryString.parse(this.props.location.search)?.prevPath);
        else
            history.push('dashboard');
        window.location.reload();
    }

    render() {
        return (
            <>
            </>
        );
    }
}

export default SuccessfulLogin;