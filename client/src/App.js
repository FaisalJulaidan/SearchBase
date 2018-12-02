import React, {Component} from 'react';
import './App.css';
import Dashboard from "./containers/Dashboard/Dashboard";
import LoginPage from './containers/Login/Login';


class App extends Component {
    // componentDidMount() {
    //     // Make a request for a user with a given ID
    //     axios.get("http://127.0.0.1:5000/api/admin/assistant/1")
    //         .then(function (response) {
    //             // handle success
    //             console.log(response);
    //         })
    //         .catch(function (error) {
    //             // handle error
    //             console.log(error);
    //         })
    // }

    render() {
        return (
            <Dashboard/>
        );
    }
}
            

export default App;
