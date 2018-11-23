import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import Button from 'antd/lib/button';
import axios from "axios";


class App extends Component {
    componentDidMount() {
        // Make a request for a user with a given ID
        axios.get("http://localhost:5000/testAPI ")
            .then(function (response) {
                // handle success
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
            .then(function () {
                // always executed
            });
    }

    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <img src={logo} className="App-logo" alt="logo"/>
                    <Button type="primary">Button</Button>
                </header>
            </div>
        );
    }
}

export default App;
