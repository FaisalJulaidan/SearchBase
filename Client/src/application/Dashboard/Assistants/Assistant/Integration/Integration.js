import React from 'react';

import {Button, Divider, Input} from "antd";

import styles from "./Integration.module.less"
import ReactDOMServer from 'react-dom/server'
import {getLink, hasher} from "helpers";
import {SwatchesPicker} from 'react-color';
import {connect} from 'react-redux';

const {TextArea} = Input;

class Integration extends React.Component {

    state = {
        source: "",
        dataName: "tsb-widget",
        assistantID: null,
        dataCircle: "#9254de",
        async: true,
        defer: true,
        isTestButtonDisabled: false
    };

    componentDidMount() {
        this.setState({
            assistantID: hasher.encode(this.props.assistant?.ID),
            source: this.getWidgetSrc()
        });
    }

    handleChange = (color) => this.setState({dataCircle: color.hex || color.target.value});

    copyScriptPaste = () => {
        const pasteArea = document.getElementById("pasteArea");
        pasteArea.select();
        document.execCommand("copy");
    };

    testIntegration = () => {
        // set time out to avoid many chatbot calling
        this.setState({isTestButtonDisabled: true},
            () => setTimeout(
                () => this.setState({isTestButtonDisabled: false}),
                1500
            )
        );
        let oldBot = document.getElementById("TheSearchBase_Chatbot");

        if (oldBot)
            this.props.removeChatbot();

        const script = document.createElement("script");

        // Development
        if (process.env.NODE_ENV === 'development')
            script.src = "http://localhost:3001/vendor/js/bundle.js";
        else {

            script.src = getLink("/static/widgets/build/vendor/js/main.5a3a2054.js");
            script.async = true;
            script.defer = true;
            script.setAttribute('directLink', '');
            script.setAttribute('data-name', this.state.dataName);
            script.setAttribute('data-id', this.state.assistantID);
            script.setAttribute('data-circle', this.state.dataCircle);
            script.setAttribute("id", "oldBotScript");
            document.body.appendChild(script);

            const link = document.createElement("link");
            link.href = getLink('/static/widgets/build/vendor/css/main.9fcdf850.css');
            link.type = "text/css";
            link.rel = "stylesheet";
            document.getElementsByTagName("head")[0].appendChild(link);
        }


        document.body.appendChild(script);
    };

    getWidgetSrc = () => {
        return getLink("/api/widgets/chatbot.js");
    };

    generateDirectLink = () => {

        if (window.location.port !== "")
            window.open(`http://localhost:5000/api/assistant/${this.state.assistantID}/chatbot_direct_link`);
        else
            window.open(getLink(`/api/assistant/${this.state.assistantID}/chatbot_direct_link`));
    };

    getChatbotScript = () => {
        return <script src={this.getWidgetSrc()}
                       data-name={this.state.dataName}
                       data-id={this.state.assistantID}
                       data-circle={this.state.dataCircle}
                       async={this.state.async}
                       defer={this.state.defer}/>
    };

    render() {
        return (
            <>
                <div className={styles.Header}>
                    <Button type={"primary"}
                            style={{marginLeft: "5px"}}
                            disabled={this.state.isTestButtonDisabled}
                            onClick={this.testIntegration}>
                        Test Chatbot Live
                    </Button>
                </div>


                <div>
                    <h2>Customize Chatbot Color:</h2>
                    <p>
                        Currently you can edit the colour setting of your assistant's button.
                        Simply pick your preferred one bellow.
                    </p>

                    <br/>
                    <SwatchesPicker color={this.state.dataCircle} onChange={this.handleChange}/>

                    <br/>
                    <p style={{paddingBottom: 5}}>Selected Color:</p>
                    <Input style={{padding: "3px", width: "60px"}} type="color" name="dataCircle"
                           value={this.state.dataCircle} onChange={this.handleChange}/>
                </div>


                <br/>
                <Divider/>
                <h2>Installation Code:</h2>
                <div>
                    <p>
                        To integrate your assistant, you must paste the pre-made code into any
                        part of your HTML source code.
                    </p>
                    <TextArea value={ReactDOMServer.renderToString(this.getChatbotScript())}
                              id={"pasteArea"}
                              style={{height: "70px", fontWeight: "600", margin: "1.5% 0"}}
                              readOnly/>
                    <Button onClick={this.copyScriptPaste} className={"ant-btn-primary"}>Copy</Button>
                    <Button style={{marginLeft: "5px"}} onClick={this.generateDirectLink}
                            className={"ant-btn-primary"}>Generate Direct Link</Button>
                </div>
            </>

        );
    }
}

function mapStateToProps(state) {
    return {
        assistantList: state.assistant.assistantList,
    };
}

export default connect(mapStateToProps)(Integration);
