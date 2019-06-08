import React from 'react';

import {Button, Col, Input, Row, Divider} from "antd";

import styles from "./Integration.module.less"
import ReactDOMServer from 'react-dom/server'
import {hasher, getLink} from "helpers";
import {SwatchesPicker} from 'react-color';
import {connect} from 'react-redux';

const {TextArea} = Input;


(function (arr) {
    arr.forEach(function (item) {
        if (item.hasOwnProperty('remove')) {
            return;
        }
        Object.defineProperty(item, 'remove', {
            configurable: true,
            enumerable: true,
            writable: true,
            value: function remove() {
                this.parentNode.removeChild(this);
            }
        })
    })
})([Element.prototype, CharacterData.prototype, DocumentType.prototype]);

const isNodeExist = (element, inArray) => {
    let isExist = false;
    for (const inArray_element of inArray)
        if (element.isEqualNode(inArray_element)) {
            isExist = true;
            break;
        }
    return isExist
};

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

    firstHead = null;

    componentDidMount() {
        this.setState({
            assistantID: hasher.encode(this.props.assistant.ID),
            source: this.getWidgetSrc()
        });
        this.firstHead = [...document.head.children];
    }

    componentWillUnmount() {
        this.removeChatbot();
    }


    handleChange = (color) => this.setState({dataCircle: color.hex || color.target.value});

    removeChatbot = () => {
        let oldBot = document.getElementById("TheSearchBase_Chatbot");
        if (oldBot) oldBot.remove();

        let oldBotScript = document.getElementById("oldBotScript");
        if (oldBotScript) oldBotScript.remove();


        let newHead = document.head.children;
        let elements = [];

        // find all new css
        for (const element of newHead)
            if (!isNodeExist(element, this.firstHead))
                elements.push(element);

        // remove all new css
        for (let i = 0; i < elements.length; i++)
            elements[i].remove();
    };

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
            this.removeChatbot();

        const script = document.createElement("script");

        script.src = this.state.source;
        script.async = this.state.async;
        script.defer = this.state.defer;
        script.setAttribute("data-name", this.state.dataName);
        script.setAttribute("data-id", this.state.assistantID);
        script.setAttribute("data-circle", this.state.dataCircle);
        script.setAttribute("id", "oldBotScript");

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
                    <Button style={{marginLeft: "5px"}}
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
