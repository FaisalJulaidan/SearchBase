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
        dataIcon: "#ffffff",
        dataCircle: "#01d1de",
        async: true,
        defer: true
    };

    componentDidMount() {
        console.log(this.props);
        this.setState({
            dataID: this.props.match.params.id,
            source: window.location.protocol + '//' + window.location.hostname + ":" + window.location.port + "/userdownloads/widget.js"
        });
    }

    handleChange = ({target}) => {
        this.setState({
            [target.name]: target.value
        });
    };

    testIntegration = () => {
        const script = document.createElement("script");

        script.src = this.state.source;
        script.async = this.state.async;
        script.defer = this.state.defer;
        script.dataName = this.state.dataName;
        script.dataID = this.state.dataID;
        script.dataIcon = this.state.dataIcon;
        script.dataCircle = this.state.dataCircle;

        console.log(script);

        document.body.appendChild(script);
    };

    render() {

        const urlPaste = (<script src={window.location.protocol + '//' +
            window.location.hostname + ":" + window.location.port + "/userdownloads/widget.js"}
                              data-name={this.state.dataName}
                              data-id={this.props.match.params.id}
                              data-icon={this.state.dataIcon}
                              data-circle={this.state.dataCircle} async={this.state.async}
                              defer={this.state.defer}/>);

        return (
            <div style={{height: '100%'}}>
                <div style={{padding: '0 5px'}}>
                    <div style={{width: '100%', height: 56, marginBottom: 10}}>
                        <Header display={"Integration"}/>
                    </div>
                </div>

                <div style={{height: 'calc(100% - 66px)', width: '100%', display: 'flex'}}>

                    <div style={{margin: 5, width: '45%'}}>

                        <div className={styles.Panel}>
                            <div className={styles.Header} style={{position: "inherit"}}>
                                <h3>Choosing your pallet</h3>
                            </div>


                            <div className={styles.Body}>

                                <p> Currently you can edit the colour settings of your assistant's button.
                                    Simply pick your preferred ones bellow.</p>
                                <div style={{display: "-webkit-inline-box"}}>

                                    <div style={{margin: "10px"}}>
                                        <input type="color" name="dataIcon" value={this.state.dataIcon}
                                               onChange={this.handleChange}/>
                                        <label htmlFor="icon">Icon</label>
                                    </div>

                                    <div style={{margin: "10px"}}>
                                        <input type="color" name="dataCircle" value={this.state.dataCircle}
                                               onChange={this.handleChange}/>
                                        <label htmlFor="circle">Circle</label>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                    <div style={{margin: 5, width: '55%'}}>

                        <div className={styles.Panel}>
                            <div className={styles.Header} style={{position: "inherit"}}>
                                <h3>Connecting your assistant</h3>
                            </div>


                            <div className={styles.Body}>
                                <p>
                                    To integrate your assistant, you must paste the pre-made code into any part of your
                                    HTML
                                    source code.
                                </p>

                                <textarea value={ReactDOMServer.renderToString(urlPaste)}
                                          style={{width: "90%", height: "90px", fontWeight: "600"}}
                                          readOnly/>
                                {urlPaste}
                                <Button onClick={this.testIntegration} className={"ant-btn-primary"}>Test Bot</Button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Integration;