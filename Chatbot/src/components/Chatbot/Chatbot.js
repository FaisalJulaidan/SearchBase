import React from "react";
import Button from "./Button/Button";
import Header from "./Header/Header";
import Flow from "./Flow/Flow";
import Input from "./Input/Input";
import axios from "axios";
import {constants} from '../../utilities/constants';
import styles from "./Chatbot.module.css";
import {Skeleton} from "antd";
import Signature from './Signature/Signature'
import 'antd/lib/skeleton/style'; // or antd/lib/button/style/css for css format file
import {detectUserType} from "../../utilities/helpers";
import * as actionTypes from "../../store/actions";
import {connect} from "react-redux";

class Chatbot extends React.Component {
    state = {
        assistant: null,
        currencies: [],
        blocks: [],
        dataTypes: [],

        sessionID: undefined,
        currentBlock: {},
        collectedData: [],
        submittedFiles: [],
        keywords: [],
        messages: [],
        solutions: [],
        selectedSolutions: [],
        solutionsReturned: 0,

        isWindowOpen: false,
        isWindowOpenAnimate: false,
        isChatbotStarted: false,
        isChatbotEnded: false,
        // always show skeleton for a moment
        showSkeleton: true,

        isFetching: false, // loading data
        isFetched: false, // data loaded successfully
        isSendingData: false,
        isFetchingSolutions: false,
        isDisabled: false,

        userTypesFreq: [], // this will be used for detecting user type intelligently
        keywordsByDataType: {},

        elapsed: 0,
        totalElapses: [],

        currentScore: 0,
        totalScore: 0.05,

        CandidateName: null,
        CandidateEmail: null,
        CandidateMobile: null,

        ClientName: null,
        ClientEmail: null,
        ClientTelephone: null,
    };

    constructor(props) {
        super(props);
        this.Flow = React.createRef();
    }

    componentDidMount() {

        // When page is left
        window.addEventListener("beforeunload", event => {
            // Submit uncompleted session only if at least one question is being answered
            if(this.state.collectedData.length > 3)
                this.endChatbot(false)
        }, false);

        const scriptTag = document.querySelector('script[data-name="tsb-widget"][data-id]');
        const fullHost = scriptTag.getAttribute("src").split("/");

        this.host = fullHost[0] + '//' + fullHost[2];
        this.assistantID = scriptTag.getAttribute("data-id");
        this.btnColor = scriptTag.getAttribute("data-circle");

        // Extra attributes.
        // test: means client is testing his chatbot and data won't be submitted at the end to the server
        // dev: means development mode will connect to the localhost even though src value is not pointing to it
        this.isTesting = scriptTag.getAttribute("test") === '';
        this.isDev = scriptTag.getAttribute("dev") === '';
        this.isDirectLink = scriptTag.getAttribute('data-directLink') === '';

        if(this.isDev) {this.host = "http://127.0.0.1:5000";}

        if (this.isDirectLink) {
            this.setState({isWindowOpen: true, isWindowOpenAnimate: true});
        }

        // Fetch assistant data (blocks...)
        this.setState({isFetching: true});
        axios.get(`${this.host}/api/assistant/${this.assistantID}/chatbot`)
            .then(res => {
                const data = res.data.data;

                if (data.isDisabled)
                    return this.setState({
                        isDisabled: true,
                        isFetching: false,
                        isFetched: true
                    });


                this.setState({
                    currencies: data.currencies,
                    assistant: data.assistant,
                    blocks: [].concat(data.assistant.Flow.groups.map(group => group.blocks)).flat(1),
                    isFetching: false,
                    isFetched: true
                });
                const {SecondsUntilPopup} = this.state.assistant;

                if (SecondsUntilPopup > 0)
                    setTimeout(() => this.openWindow(), SecondsUntilPopup * 1000);

                else if (this.isDirectLink) {
                    this.openWindow()
                }

            }).catch(error => {
            console.error("Server Error! ", error);
            this.setState({ isFetching: false, isFetched: false });
            if (this.isDev) this.setState({isFetched: true});
        });
    }

    openWindow = () => {
        this.setState(
            {isWindowOpen: true, isWindowOpenAnimate: true, start: Date.now()},
            () =>
                // only start time when window is open
                this.timer = setInterval(
                    () => this.setState({elapsed: new Date() - this.state.start}), 1000
                )
        );

        // for the first show skeleton for 1500ms then start chatbot
        // after open window hide the skeleton, then will run start chatbot
        if (!this.state.isChatbotStarted)
            setTimeout(() => {
                this.setState({showSkeleton: false});
                if (!this.state.isChatbotStarted) {
                    this.setState({isChatbotStarted: true}, () => this.startChatbot());
                }
            }, 1200);
    };

    closeWindow = () => {
        this.setState({isWindowOpenAnimate: false});

        // waits for finish the animation then remove the DOM
        setTimeout(() => {
            this.setState({isWindowOpen: false, totalElapses: this.state.totalElapses.concat([this.state.elapsed])});
            clearInterval(this.timer); // stop timer when window is close and start again when opened
        }, 500);
    };

    startChatbot = () => {
        const showFirstBlock = () => {
            // Push the the first block to the renderedBlocks
            if (this.state.blocks.length > 0) {
                const currentBlock = this.state.blocks[0];
                this.setState({currentBlock});
                this.composeAndPushMsg(currentBlock, 600);
            }
        };

        // Set the welcome message if exists
        const welcomeMsg = this.state.assistant.Message;
        if (!(welcomeMsg.length === 0))
            this.pushMessage("BOT", welcomeMsg, constants.TEXT, null, 0)
                .then(() => showFirstBlock());
        else showFirstBlock();

    };

    pushMessage = (from, msg, type, content, delay = constants.DELAY_DEFAULT) => new Promise((res) => {
        this.Flow.current.scrollToBottom(0);
        // From: BOT, USER
        // Types: Question, File Upload, Text, Solutions, Warn, Success, Failure
        const message = {from: from, type: type, text: msg, content, delay};
        const messages = this.state.messages.concat(message);
        setTimeout(() => this.setState({messages: messages}, () => {
            this.Flow.current.scrollToBottom(0);
            return res('done')
        }), delay);
    });

    // Create the message content based on the block type
    composeAndPushMsg = (block, delay=constants.DELAY_DEFAULT) => {

        const content = block.Content;
        // Check the userTypes associated with each block's dataType and record them
        this.setState({userTypesFreq:this.state.userTypesFreq.concat(block.DataType.userTypes)});


        switch (block.Type) {
            case constants.QUESTION:
                return this.pushMessage("BOT", content.text, constants.QUESTION, {
                    answers: content.answers, skippable: block.Skippable, skipText: block.SkipText
                }, delay);
            case constants.FILE_UPLOAD:
                return this.pushMessage("BOT", content.text, constants.FILE_UPLOAD, {
                    fileTypes: content.fileTypes,
                    skippable: block.Skippable, skipText: block.SkipText
                }, delay);
            case constants.USER_INPUT:
                return this.pushMessage("BOT", content.text, constants.USER_INPUT, {
                    skippable: block.Skippable, skipText: block.SkipText
                }, delay);
            case constants.SOLUTIONS:
                return this.fetchSolutions(block.Content.showTop, block.Content.databaseType);
            case constants.RAW_TEXT:
                return this.pushMessage("BOT", content.text, constants.RAW_TEXT, {}, delay)
                    .then(() => this.proceed(block.Content.action, block.Content.blockToGoID));

            default:
                return console.error("Cannot compose msg because block type is not recognize");
        }
    };


    // Move Forward with the chatbot flow
    proceed = (actionType, blockToGoID) => {
        let nextBlock = undefined;
        console.log(actionType);
        switch (actionType) {
            case "Go To Next Block":
            case "Go To Specific Block" :
            case "Go To Group" :

                // Check if the pointed block exists, if no end chat
                nextBlock = this.state.blocks.find(block => block.ID === blockToGoID);
                if (!nextBlock)
                    return this.endChatbot(true);

                this.setState({currentBlock: nextBlock});
                this.composeAndPushMsg(nextBlock);
                break;

            case "End Chat":
                this.endChatbot(true);
                break;
            default:
                console.error("Action type is not recognize");
                return;
        }
    };

    collectDataBuilder = (blockID, questionText, input, dataType, keywords, skipped = false) => {
        const {name, enumName} = dataType;
        console.log(name, enumName)
        if (!skipped){
            const kdt = {...this.state.keywordsByDataType};
            if (name in kdt) {kdt[name] = kdt[name].concat(keywords || input)}
            else {kdt[name] = keywords}
            this.setState({keywordsByDataType: kdt});

            // Collect primary data separate from keywordsByDataType
            if (new RegExp(['Name','Email', 'Mobile', 'Telephone'].join("|")).test(enumName)) {
                // At least one match
                console.log("HERE")
                this.setState({[enumName]: input})
            }
        }
        return { blockID, questionText, input: input.trim(), dataType: name, keywords }
    };

    submitInput = (input, inputKeywords) => {
        const currentBlock = this.state.currentBlock;

        // Collect data
        if (currentBlock.StoreInDB) {
            const data = this.collectDataBuilder(currentBlock.ID,
                currentBlock.Content.text, input, currentBlock.DataType, inputKeywords);

            // Aggregate collected data
            const collectedData = this.state.collectedData.concat(data);
            const keywordsArray = this.state.keywords.concat(inputKeywords);

            // Add to score based on keywords
            let totalScore  = 0, currentScore  = 0;
            const blockKeywords = currentBlock.Content.keywords || [];
            const inputKeywordsLowered = inputKeywords.map(k => k.toLowerCase());

            if(blockKeywords.length > 0) {
                totalScore = Math.round(blockKeywords.length / 2);
                currentScore = blockKeywords.filter(value => inputKeywordsLowered
                    .includes(value.toLowerCase()))
                    .length
            }

            // Set the state with the new values
            this.setState({
                collectedData,
                keywords: keywordsArray,
                currentScore: this.state.currentScore + currentScore,
                totalScore: this.state.totalScore + totalScore
            });
        }

        // Push user input as a message and if there is an afterMessage push it too
        this.pushMessage("USER", input.trim(), "Text", null, 0)
            .then(() => {
                if (currentBlock.Content.afterMessage.trim() !== "")
                    this.pushMessage("BOT", currentBlock.Content.afterMessage, "Text", null)
                        .then(() => this.proceed(currentBlock.Content.action, currentBlock.Content.blockToGoID));
                else
                    this.proceed(currentBlock.Content.action, currentBlock.Content.blockToGoID);
            });
    };

    submitAnswer = (selectedAnswer, otherAnswers) => {

        const currentBlock = this.state.currentBlock;
        const {text, action, keywords, blockToGoID, afterMessage} = selectedAnswer;
        // Adds the answer text as part of the keywords list
        const modifiedKeywords = keywords.concat(text.trim().split(" ").filter(n => n));
        // Collect data
        const data = this.collectDataBuilder(currentBlock.ID,
            currentBlock.Content.text, text, currentBlock.DataType, modifiedKeywords);

        // Set gathered data to the state
        const collectedData = this.state.collectedData.concat(data);
        const keywordsArray = this.state.keywords.concat(modifiedKeywords);

        this.setState({
            collectedData,
            keywords: keywordsArray,
            currentScore: this.state.currentScore + selectedAnswer.score,
            totalScore: this.state.totalScore + Math.max(...otherAnswers.map(answer => answer.score))
        });

        // Update the flow
        this.pushMessage("USER", text.trim(), "Text", null, 0)
            .then(() => {
                // Print after message if there, then proceed()
                if (afterMessage.trim() !== "")
                    this.pushMessage("BOT", afterMessage, "Text", null)
                        .then(() => this.proceed(action, blockToGoID));
                else // Move forward to the next block
                    this.proceed(action, blockToGoID);
            });
    };

    submitFile = file => {
        const currentBlock = this.state.currentBlock;
        // Collect data
        const data = this.collectDataBuilder(currentBlock.ID,
            currentBlock.Content.text, "&FILE_UPLOAD&", currentBlock.DataType, ["&FILE_UPLOAD&"]);
        // Set gathered data to the state
        const collectedData = this.state.collectedData.concat(data);
        const submittedFiles = this.state.submittedFiles.concat(file);

        this.setState({submittedFiles, collectedData});

        // Push user input as a message and if there is an afterMessage as well
        this.pushMessage("USER", file.name, "Text", null, 0)
            .then(() => {
                if (currentBlock.Content.afterMessage.trim() !== "")
                    this.pushMessage("BOT", currentBlock.Content.afterMessage, "Text", null)
                        .then(() => this.proceed(currentBlock.Content.action, currentBlock.Content.blockToGoID));
                else
                    this.proceed(currentBlock.Content.action, currentBlock.Content.blockToGoID);
            });
    };

    selectSolution = solution => {
        let messages = JSON.parse(JSON.stringify(this.state.messages));
        messages[messages.length - 1].content
            .solutions.find(s => s.id === solution.id).selected = !(!!solution.selected);
        this.setState({messages});
    };

    submitSolutions = (solutions) => {

        const {currentBlock} = this.state;

        // When solutions selection block is the last one, solve the issue of resubmitting
        if (!currentBlock.DataType) return;

        // Wait for selected solutions to be set then proceed to the next block
        this.setState({selectedSolutions: this.state.selectedSolutions.concat(solutions)}, () => {
            // Collect data after the users has selected a solution
            const data = this.collectDataBuilder(currentBlock.ID, "Database scanning",
                `Selected ${solutions.length} solution(s)`, currentBlock.DataType, []
            );

            // Set gathered data to the state
            this.setState({collectedData: this.state.collectedData.concat(data)});

            if (currentBlock.Content.afterMessage.trim() !== "") // proceed with after message
                this.pushMessage("BOT", currentBlock.Content.afterMessage, "Text", null, 0)
                    .then(() => this.proceed(currentBlock.Content.action, currentBlock.Content.blockToGoID));
            else
                this.proceed(currentBlock.Content.action, currentBlock.Content.blockToGoID);
        });
    };

    skip = (text) => {

        // Collect data by answering the question as skipped
        const currentBlock = this.state.currentBlock;

        const data = this.collectDataBuilder(currentBlock.ID,
            currentBlock.Content.text || "Database scanning",
            text, currentBlock.DataType, text.trim().split(" ").filter(n => n), true);

        // Process score
        let totalScore  = 0;
        switch (currentBlock.Type) {
            case constants.QUESTION:
              totalScore = Math.max(...currentBlock.Content.answers.map(answer => answer.score));
              break;
            case constants.USER_INPUT:
                totalScore = Math.round(currentBlock.Content.keywords.length / 2);
                break;
        }

        // Set gathered data to the state
        this.setState({
            collectedData: this.state.collectedData.concat(data),
            totalScore: this.state.totalScore + totalScore
        });

        // Answer the question as skipped and move forward to the next block
        this.pushMessage("USER", text, "Text", null, 0)
            .then(() => {
                this.proceed(currentBlock.SkipAction, currentBlock.SkipBlockToGoID);
            })
    };

    // Fetch solutions based on collected keywords from user's inputs
    fetchSolutions = (showTop, databaseType) => {
        const currentBlock = this.state.currentBlock;
        const data = {
            collectedData: this.state.collectedData,
            keywords: this.state.keywords,
            showTop: showTop,
            keywordsByDataType: this.state.keywordsByDataType,
            databaseType: databaseType
        };
        this.setState({isFetchingSolutions: true});

        axios.post(`${this.host}/api/assistant/${this.assistantID}/chatbot/solutions`, data)
            .then(res => {
                // This condition ensures if the server returns null, then don't concat that null to the array because null going to be counted as one but instead make empty list
                let solutions = res.data.data ? res.data.data : [];

                if (solutions.length) {
                    // Check the userTypes associated with the solutions and record them
                    this.setState({userTypesFreq:this.state.userTypesFreq.concat(solutions[0].databaseType.userTypes)});
                }

                this.setState({
                    solutions,
                    isFetchingSolutions: false,
                    solutionsReturned: this.state.solutionsReturned + solutions.length
                });

                // Enquire will go to the next block while store the selected solution into an array which is going
                // to be passed within the session's collectedData
                this.pushMessage("BOT", "", constants.SOLUTIONS, {
                    solutions, skippable: currentBlock.Skippable, skipText: currentBlock.SkipText
                }).then(() => {
                    // if no solution found in server
                    if (!solutions[0])
                        this.proceed(currentBlock.Content.action, currentBlock.Content.blockToGoID);
                });

            }).catch(() => {
            this.pushMessage("BOT", "sorry an error occurred!", "Text", null);
            this.setState({isFetchingSolutions: false});
        });
    };

    // Send user input to the back-end
    sendData = (userType, isConversationCompleted) => {

        // Ensure sending data once at the end to prevent with spamming
        // + Don't send data if chatbot is in testing mode so the script tag has "test" attribute in it
        if (this.isTesting || this.state.sessionID) {return;}

        console.log("Sending data...");
        const {totalElapses, collectedData, keywords, solutions, keywordsByDataType,
            elapsed, selectedSolutions, currentScore, totalScore} = this.state;
        clearInterval(this.timer);

        const {CandidateName, CandidateEmail, CandidateMobile, ClientName, ClientEmail, ClientTelephone} = this.state;

        let name, email, phone;
        if (userType === 'Candidate'){
            name = CandidateName;
            email = CandidateEmail;
            phone = CandidateMobile;
        }

        if (userType === 'Client'){
            name = ClientName;
            email = ClientEmail;
            phone = ClientTelephone;
        }


        const data = {
            collectedData: collectedData,
            keywords: keywords,
            solutionsReturned: solutions.length,
            selectedSolutions: selectedSolutions,
            userType: userType,
            keywordsByDataType: keywordsByDataType,
            isConversationCompleted: isConversationCompleted,
            score: isConversationCompleted && totalScore > 0 ? currentScore / totalScore : 0.05,
            timeSpent: Math.floor((totalElapses[0] ? totalElapses.reduce((total, num) => total += num) : elapsed) / 1000),
            hasFiles: this.state.submittedFiles.length > 0,

            // Primary data ->
            name: name || null,
            email: email || null,
            phone: phone || null,
        };

        this.setState({isSendingData: true});

        axios.post(`${this.host}/api/assistant/${this.assistantID}/chatbot`, data)
            .then(res => {

                const { sessionID } = res.data.data;
                this.setState({isSendingData: false, sessionID });
                // Send submitted files
                const {submittedFiles} = this.state;
                if(submittedFiles.length > 0){
                    this.sendFile(this.state.submittedFiles, sessionID)
                }
            })
            .catch(error => {
                console.error(error.response.data);
                this.pushMessage("BOT", "sorry I couldn't send your data","Failure", null);
                this.setState({isSendingData: false});
            });
    };

    sendFile = (files, sessionID) => {

        const formData = new FormData();
        const config = {headers: {'content-type': 'multipart/form-data'}};
        files.forEach(file => formData.append('file',file, file.name));

        axios.post(`${this.host}/api/assistant/${this.assistantID}/session/${sessionID}/file`, formData, config)
            .then(res => {
                console.log("Files sent successfully!");
            })
            .catch(error => {
                console.error(error.response.data);
                // this.pushMessage("BOT", "sorry I couldn't send your data","Failure", null);
            });
    };

    // Start the conversation again
    reset = () => {
        console.log("Chatbot refreshed");
        clearInterval(this.timer);
        this.openWindow();
        this.setState({
            sessionID: undefined,
            currentBlock: {},
            collectedData: [],
            submittedFiles: [],
            keywords: [],
            messages: [],

            userTypesFreq: [],
            keywordsByDataType: {},

            selectedSolutions: [],
            elapsed: 0,
            totalElapses: [],

            currentScore: 0,
            totalScore: 0.05,

            CandidateName: null,
            CandidateEmail: null,
            CandidateMobile: null,

            ClientName: null,
            ClientEmail: null,
            ClientTelephone: null,

            isChatbotEnded: false,
        }, () => this.startChatbot());
    };

    // End the chatbot flow
    endChatbot = (isConversationCompleted) => {

        const detectedUserTypes = detectUserType(this.state.userTypesFreq);
        let userType = "Unknown"; // default
        if (detectedUserTypes.length === 1){
            userType = detectedUserTypes[0];
        }
        this.sendData(userType, isConversationCompleted);
        this.setState({currentBlock: {}, isChatbotEnded: true});
    };

    render() {
        const {assistant} = this.state;
        const topBarText = assistant ? assistant.TopBarText: '';
        const showSkeleton = (<div className={this.isDirectLink ? styles.Chatbot_DirectLink_Container : ''}>
            <div
                className={[
                    this.state.isWindowOpenAnimate ? styles.ZoomIn : styles.ZoomOut,
                    this.isDirectLink ? styles.Chatbot_DirectLink : styles.Chatbot
                ].join(' ')}>
                <Header assistant={assistant}
                        reseted={this.reset}
                        closed={this.closeWindow}
                        topBarText={topBarText}
                        isDirectLink={this.isDirectLink}/>
                <div style={{padding: '0 20px'}}>
                    <Skeleton active paragraph={{rows: 4}}/>
                    <Skeleton active paragraph={{rows: 2}}/>
                    <Skeleton active paragraph={{rows: 3}}/>
                </div>
            </div>
        </div>);

        if (this.state.isWindowOpen)
            if (this.state.showSkeleton && !(this.state.isChatbotStarted)) return showSkeleton;
            else return (
                <div className={this.isDirectLink ? styles.Chatbot_DirectLink_Container : ''}>
                    <div className={[
                        this.state.isWindowOpenAnimate ? styles.ZoomIn : styles.ZoomOut,
                        this.isDirectLink ? styles.Chatbot_DirectLink : styles.Chatbot
                    ].join(' ')}>
                        <Header reseted={this.reset} closed={this.closeWindow}
                                assistant={assistant}
                                topBarText={topBarText}
                                isDirectLink={this.isDirectLink}/>
                        <Flow answerClicked={this.submitAnswer}
                              selectSolution={this.selectSolution}
                              submitSolutions={this.submitSolutions}
                              isFetchingSolutions={this.state.isFetchingSolutions}
                              skipped={this.skip}
                              messages={this.state.messages}
                              ref={this.Flow}/>
                        <Input currentBlock={this.state.currentBlock}
                               inputSubmitted={this.submitInput}
                               currencies={this.state.currencies}
                               fileSubmitted={this.submitFile}/>
                        <Signature/>
                    </div>
                </div>
            );

        return <Button isWaiting={this.state.isFetched} clicked={this.openWindow} btnColor={this.btnColor}
                       disabled={this.state.isDisabled}/>
    }
}


const mapStateToProps = state => {
    return {
        isBotTyping: state.isBotTyping
    }
};

const mapDispatchToProps = dispatch => {
    return {
        onIsBotTypingUpdate: (value) => {
            dispatch({type: actionTypes.UPDATE_IS_BOT_TYPING, payload: {value}});
            return Promise.resolve();
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Chatbot);
