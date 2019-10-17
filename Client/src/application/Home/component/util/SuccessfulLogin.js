import React, {Component} from 'react';
import queryString from 'query-string';

class SuccessfulLogin extends Component {

    componentDidMount() {
        window.location.replace(queryString.parse(this.props.location.search)?.prevPath || '/dashboard');
    }

    render() {
        return (
            <>
            </>
        );
    }
}

export default SuccessfulLogin;