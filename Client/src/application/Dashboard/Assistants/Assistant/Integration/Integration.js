import React from 'react';

import {Button, Divider, Input} from "antd";

import styles from "./Integration.module.less"
import {getLink, hasher} from "helpers";
import {SwatchesPicker} from 'react-color';
import {connect} from 'react-redux';

const {TextArea} = Input;

class Integration extends React.Component {

    state = {
        dataName: "tsb-widget",
        assistantID: null,
        dataCircle: "#9254de",
        async: true,
        defer: true,
        isTestButtonDisabled: false,
    };

    componentDidMount() {
        this.setState({
            assistantID: hasher.encode(this.props.assistant?.ID),
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

        const s = document.createElement("script");
        s.setAttribute('data-name', this.state.dataName);
        s.setAttribute('data-id', this.state.assistantID);
        s.setAttribute('data-circle', this.state.dataCircle);

        // Development
        if (process.env.NODE_ENV === 'development') {
            s.src = getLink("/vendor/js/bundle.js");
            s.setAttribute("id", "oldBotScript");
        }
        s.src = getLink("/api/widgets/chatbot");

        document.body.appendChild(s);
    };

    generateDirectLink = () => window.open(getLink(`/chatbot_direct_link/${this.state.assistantID}`));

    getChatbotScript = () => `<script>const s=document.createElement("script");s.src=getLink("/api/widgets/chatbot");s.setAttribute('data-name','${this.state.dataName}');s.setAttribute('data-id','${this.state.assistantID}');s.setAttribute('data-circle','${this.state.dataCircle}');document.body.appendChild(s);</script>`;

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
                    <TextArea value={this.getChatbotScript()}
                              onClick={() => {
                                  console.log(this.getChatbotScript())
                              }}
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
