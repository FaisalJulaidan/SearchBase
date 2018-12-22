import React from 'react';
import {Form, Button, message, Tabs} from "antd";
import "./Integration.less"
import styles from "./Integration.module.less"
import ReactDOMServer from 'react-dom/server'

class Integration extends React.Component {

    state = {
        source: "",
        dataName: "tsb-widget",
        dataID: "assistantid",
        dataIcon: "#fff",
        dataCircle: "#4B5B71",
        async: true,
        defer: true,
        fullURL:""
    };

    componentDidMount() {
        console.log(this.props);
        this.setState({
            dataID: this.props.match.params.id,
            source: window.location.protocol + '//' + window.location.hostname + ":" + window.location.port + "/userdownloads/widget.js",
            fullURL: ReactDOMServer.renderToString( <script src={window.location.protocol + '//' +
                    window.location.hostname + ":" + window.location.port + "/userdownloads/widget.js"}
                                                            data-name={this.state.dataName} data-id={this.props.match.params.id}
                    data-icon={this.state.dataIcon} data-circle={this.state.dataCircle} async={this.state.async}
                    defer={this.state.defer}/> )
        });
    }

    render() {

        const urlPaste = this.state.fullURL;

        return (
            <div style={{height: '100%'}}>
                <div className={styles.Panel}>
                    <div className={styles.Panel_Header}>
                        <div>
                            <h3>Integration</h3>
                            <p>This is where you will find what you need to integrate your assistant into your website
                                and instructions on how to do it. You will also find useful features like locally
                                testing it or changing the button color scheme.</p>
                        </div>
                    </div>

                    <div className={styles.Panel_Body} style={{overflowY: "auto"}}>
                        <h3>Connecting your assistant.</h3>
                        <p>
                            To Connect your assistant, you must paste the pre-made code into any part of your HTML
                            source code.
                        </p>

                        <textarea value={urlPaste} style={{width:"600px", height:"90px", fontWeight: "600"}} readOnly/>
                    </div>
                </div>
            </div>
        );
    }
}

export default Integration;