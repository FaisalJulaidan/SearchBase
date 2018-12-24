import React from 'react';
import {Form, Button, message, Tabs} from "antd";
import "./Integration.less"
import styles from "./Integration.module.less"
import ReactDOMServer from 'react-dom/server'
import Groups from "../Flow/Groups/Groups";
import Blocks from "../Flow/Blocks/Blocks";
import Header from "./Header/Header"

class Integration extends React.Component {

    state = {
        source: "",
        dataName: "tsb-widget",
        dataID: "assistantid",
        dataIcon: "#fff",
        dataCircle: "#4B5B71",
        async: true,
        defer: true,
        fullURL: ""
    };

    componentDidMount() {
        console.log(this.props);
        this.setState({
            dataID: this.props.match.params.id,
            source: window.location.protocol + '//' + window.location.hostname + ":" + window.location.port + "/userdownloads/widget.js",
            fullURL: ReactDOMServer.renderToString(<script src={window.location.protocol + '//' +
            window.location.hostname + ":" + window.location.port + "/userdownloads/widget.js"}
                                                           data-name={this.state.dataName}
                                                           data-id={this.props.match.params.id}
                                                           data-icon={this.state.dataIcon}
                                                           data-circle={this.state.dataCircle} async={this.state.async}
                                                           defer={this.state.defer}/>)
        });
    }

    render() {

        const urlPaste = this.state.fullURL;

        return (
            <div style={{height: '100%'}}>
                <div style={{padding: '0 5px'}}>
                    <div style={{height: 56, marginBottom: 10}}>
                        <Header display={"Integration"}/>
                    </div>
                </div>

                <div style={{height: 'calc(100% - 66px)', display: 'flex'}}>

                    <div style={{margin: 5, width: '45%'}}>

                        <div className={styles.Panel}>
                            <div className={styles.Header} style={{position:"inherit"}}>
                                <h3>Choosing your pallet</h3>
                            </div>


                            <div className={styles.Body}>

                                <p> Currently you can edit the colour settings of your assistant's button.
                                    Simply pick your preferred ones bellow.</p>
                                <div style={{display: "-webkit-inline-box"}}>

                                    <div style={{margin: "10px"}}>
                                        <input type="color" id="icon" name="color"
                                               value="#ffffff"/>
                                        <label htmlFor="icon">Icon</label>
                                    </div>

                                    <div style={{margin: "10px"}}>
                                        <input type="color" id="circle" name="color"
                                               value="#4B5B71"/>
                                        <label htmlFor="circle">Circle</label>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                <div style={{margin: 5, width: '55%'}}>

                    <div className={styles.Panel}>
                        <div className={styles.Header} style={{position:"inherit"}}>
                            <h3>Connecting your assistant</h3>
                        </div>


                        <div className={styles.Body}>
                            <p>
                                To integrate your assistant, you must paste the pre-made code into any part of your HTML
                                source code.
                            </p>

                            <textarea value={urlPaste} style={{width: "90%", height: "90px", fontWeight: "600"}}
                                      readOnly/>
                        </div>

                    </div>
                </div>
                </div>
            </div>
        );
    }
}

export default Integration;