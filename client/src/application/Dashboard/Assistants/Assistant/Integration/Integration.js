import React from 'react';

import {Button, Col, Input, Row} from "antd";
import Header from "../../../../../components/Header/Header"

import styles from "./Integration.module.less"
import ReactDOMServer from 'react-dom/server'
import {hasher} from "../../../../../helpers"
import {SwatchesPicker} from 'react-color';

import "./Integration.less"

const {TextArea} = Input;


class Integration extends React.Component {

    state = {
        source: "",
        dataName: "tsb-widget",
        dataID: "assistantid",
        // dataIcon: "#ffffff",
        dataCircle: "#9254de",
        async: true,
        defer: true
    };

    componentDidMount() {
        this.setState({
            dataID: hasher.encode(this.props.match.params.id),
            source: this.getWidgetSrc()
        });
    }

    componentWillUnmount(){
        this.removeChatbot();
    }

    handleChange = (color) => this.setState({dataCircle: color.hex || color.target.value});

    removeChatbot = () => {
        let oldBot = document.getElementById("TheSearchBase_Chatbot");
        if (oldBot) oldBot.remove();
        let oldBotScript = document.getElementById("oldBotScript");
        if (oldBotScript) oldBotScript.remove();
    };

    copyScriptPaste = () => {
        const pasteArea = document.getElementById("pasteArea");
        pasteArea.select();
        document.execCommand("copy");
    };

    testIntegration = () => {
        this.removeChatbot();
        const script = document.createElement("script");

        script.src = this.state.source;
        script.async = this.state.async;
        script.defer = this.state.defer;
        script.setAttribute("data-name", this.state.dataName);
        script.setAttribute("data-id", this.state.dataID);
        // script.setAttribute("data-icon", this.state.dataIcon);
        script.setAttribute("data-circle", this.state.dataCircle);
        script.setAttribute("id", "oldBotScript");

        document.body.appendChild(script);
    };


    getWidgetSrc = () => {
        // include the colon if there is port number, which means localhost and not real server
        let colon = "";
        if (window.location.port !== "") {colon = ":";}
        const {protocol, port, hostname} = window.location;
        return protocol + '//' + hostname + colon + port + "/userdownloads/widget.js";
    };

    generateDirectLink = () => {
        const {protocol, port, hostname} = window.location;
        let colon = "";
        if (window.location.port !== "") colon = ":";
        if (port === "3000")
            window.open(`${protocol}//${hostname}${colon}5000/assistant/YJkLo/chatbot_direct_link`);
        else
            window.open(`${protocol}//${hostname}${colon}${port}/assistant/YJkLo/chatbot_direct_link`);

    };

    getChatbotScript = () => {
        return <script src={this.getWidgetSrc()}
                       data-name={this.state.dataName}
                       data-id={this.state.dataID}
                       // data-icon={this.state.dataIcon}
                       data-circle={this.state.dataCircle}
                       async={this.state.async}
                       defer={this.state.defer}/>
    };

    render() {
        return (
            <div style={{height: '100%'}}>
                <Header display={`Integration`}/>

                <div className={styles.Panel_Body_Only}>
                    <div style={{marginRight: 5, width: '45%'}} className={styles.Panel}>

                        <div className={styles.Panel_Header} style={{position: "inherit"}}>
                            <h3>Choosing your Assistant's looks</h3>
                        </div>

                        <div className={styles.Panel_Body}>
                            <Row type="flex" justify="center">
                                <Col>
                                    <p> Currently you can edit the colour setting of your assistant's button.
                                        Simply pick your preferred one bellow.</p>
                                </Col>
                            </Row>

                            <br/>

                            <Row type="flex" justify="center" style={{marginBottom: 50}}>
                                <Col>
                                    <SwatchesPicker color={this.state.dataCircle} onChange={this.handleChange}/>
                                </Col>
                            </Row>

                            <Row type="flex" justify="center">
                                <Col>
                                    <p style={{lineHeight: '27px', marginRight: 5}}>Selected Color:</p>
                                </Col>
                                <Col>
                                    <Input style={{padding: "3px", width: "60px"}} type="color" name="dataCircle"
                                           value={this.state.dataCircle} onChange={this.handleChange}/>
                                </Col>

                            </Row>
                        </div>
                    </div>


                    <div style={{marginLeft: 5, width: '55%'}} className={styles.Panel}>

                        <div className={styles.Panel_Header} style={{position: "inherit"}}>
                            <h3>Connecting your assistant</h3>
                        </div>

                        <div className={styles.Panel_Body} style={{textAlign: 'center'}}>
                            <p style={{textAlign: 'left'}}>
                                To integrate your assistant, you must paste the pre-made code into any part of your
                                HTML
                                source code.
                            </p>

                            <TextArea value={ReactDOMServer.renderToString(this.getChatbotScript())}
                                      id={"pasteArea"}
                                      style={{width: "100%", height: "110px", fontWeight: "600", margin: "1.5% 0"}}
                                      readOnly/>
                            <Button onClick={this.copyScriptPaste} className={"ant-btn-primary"}>Copy</Button>
                            <Button style={{marginLeft: "5px"}} onClick={this.testIntegration}
                                    className={"ant-btn-primary"}>Test</Button>
                            <Button style={{marginLeft: "5px"}} onClick={this.generateDirectLink}
                                    className={"ant-btn-primary"}>Generate Direct Link</Button>
                        </div>
                    </div>
                </div>

            </div>
        );
    }
}

export default (Integration);