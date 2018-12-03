import React from 'react';
import { connect } from 'react-redux';

import { authActions } from '../../store/actions/auth.action';

class LoginPage extends React.Component {

    state = {
        email: '',
        password: '',
        submitted: false
    };


    handleChange = (e) => {
        const { name, value } = e.target;
        this.setState({ [name]: value });
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.setState({ submitted: true });
        const { email, password } = this.state;
        if (email && password) {
            this.props.dispatch(authActions.login(email, password));
        }
    };

    handleLogout = () => {
        this.props.dispatch(authActions.logout());
    };

    render() {
        const { isLoggingIn } = this.props;
        console.log(isLoggingIn);
        const { email, password, submitted } = this.state;
        return (
            <div className="col-md-6 col-md-offset-3">
                <div className="alert alert-info">
                    Email: test<br />
                    Password: test
                </div>
                <h2>Login</h2>
                <form name="form" onSubmit={this.handleSubmit}>
                    <div>
                        <label htmlFor="email">Email</label>
                        <input type="text"  name="email" value={email} onChange={this.handleChange} />
                        {submitted && !email &&
                            <div className="help-block">Email is required</div>
                        }
                    </div>
                    <div className={'form-group' + (submitted && !password ? ' has-error' : '')}>
                        <label htmlFor="password">Password</label>
                        <input type="password" name="password" value={password} onChange={this.handleChange} />
                        {submitted && !password &&
                            <div className="help-block">Password is required</div>
                        }
                    </div>
                    <div className="form-group">
                        <button>Login</button>
                    </div>
                </form>
                <button onClick={this.handleLogout}>Logout</button>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        isLoggingIn: state.auth.isLoggingIn
    };
}

export default connect(mapStateToProps)(LoginPage);
