import axios from 'axios';
import queryString from 'query-string';
// Constants
import * as messageTypes from '../constants/MessageType';
import * as flowAttributes from '../constants/FlowAttributes';
import * as solutionAttributes from '../constants/SolutionAttributes';
import * as constants from '../constants/Constants';
// Utils
import { promiseWrapper } from './wrappers';
import { getServerDomain } from './index';


export const dataHandler = (() => {
    let instance;
    const init = () => {
        const CancelToken = axios.CancelToken;
        let source;

        let assistantID = undefined;
        let sessionID = undefined;
        let fetchedSolutions = []; // all solutions fetched so far
        let timeElapsed = 0;
        let messages = []; // updated constantly by Flow.js useEffect hook

        const setAssistantID = (id) => assistantID = id;

        const setSessionID = (id) => sessionID = id;

        const incrementTimeElapsed = (value) => timeElapsed += value;

        const resetTimeElapsed = () => timeElapsed = 0;

        const updateMessages = (updatedMessages) => {
            messages = updatedMessages;
        };

        const fetchSolutions = async (showTop, databaseType) => {
            let resolve = { cancelled: false, solutions: [] };
            source = CancelToken.source();
            const result = processMessages(false);
            const payload = {
                collectedData: result.collectedData,
                keywords: result.keywords,
                showTop: showTop,
                keywordsByDataType: result.keywordsByDataType,
                databaseType: databaseType
            };

            let headers = new Headers();
            headers.append('Content-Type', 'application/json');
            headers.append('Accept', 'application/json');

            const { data, error } = await promiseWrapper(
                axios.post(`${getServerDomain()}/api/assistant/${assistantID}/chatbot/solutions`, payload, {
                    headers,
                    cancelToken: source.token
                })
            );

            const solutions = data ? data.data.data : []; // :) // lol faisal 🔫
            if (axios.isCancel(error)) {
                console.log('cancelled');
                resolve.cancelled = true;
            }
            if (error) {
                console.log('fetchSolutions: ', error);
            }

            // Check the userTypes associated with the solutions and record them
            fetchedSolutions = fetchedSolutions.concat(solutions);
            resolve.solutions = solutions;
            return resolve;
        };

        const cancelRequest = (message) => {
            if (source) source.cancel(message);
        };

        const sendData = async (completed) => {
            source = CancelToken.source();
            let cancelled;
            const result = processMessages(completed); // loop messages
            if ((!completed && result.collectedData.length < 1) || sessionID) return { cancelled };

            const cancel = {
                cancelToken: source.token
            };

            // Check if chatbot sent directly to specific candidate for update (e.g. sent through campaign)
            if (window.location.href.includes('chatbot_direct_link')) {
                let params = queryString.parse(window.location.search);
                if(params['candidate']) {
                    result['candidateInfo'] = params['candidate'];
                }
            }

            // Process uploaded files and append it to the request via fromData
            const formData = new FormData();
            const config = { headers: { 'content-type': 'multipart/form-data' }, ...cancel };
            const files = result.submittedFiles;

            files.forEach(file => formData.append('file', file.file, file.file.name));
            formData.append('keys', files.map(file => file.key).join(','));
            formData.append('conversation', JSON.stringify(result));
            // send data to server
            const { data, error } = await promiseWrapper(axios.post(`${getServerDomain()}/api/assistant/${assistantID}/chatbot`, formData, config));

            if (axios.isCancel(error)) {
                console.log('axios cancelled');
                cancelled = true;
            }
            if (error) {
                console.log('SendData: ', error);
            }

            return { dataSent: !!sessionID, cancelled };
        };

        const processMessages = (completed) => {
            let userType = 'Unknown';
            let collectedData = [];
            let collectedKeywords = [];
            let keywordsByDataType = {};
            let submittedFiles = [];
            let selectedSolutions = [];
            let recordedUserTypes = [];
            let _curScore = 0;
            let _totalScore = 0;
            const personalData = {
                CandidateName: null,
                CandidateEmail: null,
                CandidateMobile: null,
                ClientName: null,
                ClientEmail: null,
                ClientTelephone: null
            };

            const __collectData = (blockID, questionText, input, dataType, keywords, skipped, extras = {}) => {
                const { name, enumName } = dataType;
                if (!skipped) {
                    const kdt = { ...keywordsByDataType };
                    if (name in kdt) {
                        kdt[name] = kdt[name].concat(keywords || input);
                    } else {
                        kdt[name] = keywords;
                    }
                    keywordsByDataType = kdt;

                    // Collect personal data separate from keywordsByDataType
                    if (new RegExp(['Name', 'Email', 'Mobile', 'Telephone'].join('|')).test(enumName)) {
                        // At least one match
                        personalData[enumName] = input;
                    }
                }
                collectedData = collectedData.concat({
                    blockID,
                    questionText,
                    input: input.trim(),
                    dataType: name,
                    keywords,
                    ...extras
                });
            };

            const __detectUserType = () => {
                let userType = 'Unknown'; // default
                recordedUserTypes = recordedUserTypes.filter(t => t !== userType);
                if (recordedUserTypes.length === 0)
                    return userType;

                let types = {};
                let maxCount = 1;
                for (let type of recordedUserTypes) {
                    let key = type;
                    if (types[key] == null)
                        types[key] = 1;
                    else
                        types[key]++;
                    if (types[key] > maxCount)
                        maxCount = types[key];
                }
                types = Object.keys(types).filter(key => types[key] === maxCount);
                if (types.length === 1)
                    userType = types[0];
                return userType;
            };

            const __recordUserTypes = (types) => {
                recordedUserTypes = recordedUserTypes.concat(types);
            };

            const __accumulateScore = (earnedScore, total) => {
                _curScore += earnedScore;
                _totalScore += total;
            };

            const __processQuestion = (message) => {
                const { blockRef, content, text } = message;
                const answers = blockRef[flowAttributes.CONTENT][flowAttributes.CONTENT_ANSWERS];

                // there will be no selectedAnswer when question skipped
                let keywords = content.selectedAnswer ? content.selectedAnswer.keywords : [];
                let score = content.selectedAnswer ? content.selectedAnswer.score : 0;

                // Adds the answer text as part of the keywords list
                let modifiedKeywords = [];
                if (!content.skipped)
                    modifiedKeywords = keywords.concat(text.trim().split(' ').filter(n => n));

                __collectData(
                    blockRef[flowAttributes.ID],
                    blockRef[flowAttributes.CONTENT][flowAttributes.CONTENT_TEXT],
                    text,
                    blockRef[flowAttributes.DATA_TYPE],
                    modifiedKeywords,
                    content.skipped);
                __accumulateScore(score, Math.max(...answers.map(answer => answer.score)));
            };

            const __processPredefinedAnswers = (message) => {
                const { blockRef, content, text } = message;
                const answers = blockRef[flowAttributes.CONTENT][flowAttributes.CONTENT_TYPES];

                // there will be no selectedAnswer when question skipped
                let keywords = content.selectedAnswer ? [content.selectedAnswer.value] : [];
                let score = content.selectedAnswer ? content.selectedAnswer.score : 0;
                let answer = content.skipped ? text : content.selectedAnswer.value;

                // if the question type is UserType and not skipped, set the UserType
                if (blockRef[flowAttributes.TYPE] === messageTypes.USER_TYPE && !content.skipped) {
                    userType = answer;
                }

                // Adds the answer text as part of the keywords list
                // let modifiedKeywords = [];
                // if (!content.skipped) {
                //     modifiedKeywords = keywords.concat(text.trim().split(' ').filter(n => n));
                // }

                __collectData(
                    blockRef[flowAttributes.ID],
                    blockRef[flowAttributes.CONTENT][flowAttributes.CONTENT_TEXT],
                    answer,
                    blockRef[flowAttributes.DATA_TYPE],
                    keywords,
                    content.skipped);
                __accumulateScore(score, Math.max(...answers.map(answer => answer.score)));
            };

            const __processUserInput = (message) => {
                const { blockRef, content, text } = message;
                const { input } = content;
                let keywords = text.trim().split(' ').filter(n => n);

                switch (blockRef[flowAttributes.DATA_TYPE][flowAttributes.DATA_TYPE_VALIDATION]) {
                    case constants.SALARY:
                        keywords = [input];
                }
                __collectData(
                    blockRef[flowAttributes.ID],
                    blockRef[flowAttributes.CONTENT][flowAttributes.CONTENT_TEXT],
                    text,
                    blockRef[flowAttributes.DATA_TYPE],
                    keywords,
                    content.skipped);

                // count keywords matched and added it to score
                const blockKeywords = blockRef[flowAttributes.CONTENT][flowAttributes.CONTENT_KEYWORDS] || [];
                const keywordsLowered = !content.skipped ? keywords.map(k => k.toLowerCase()) : []; // user input
                if (blockKeywords.length > 0) {
                    const totalScore = Math.round(blockKeywords.length / 2);
                    const matches = blockKeywords.filter(value => keywordsLowered
                        .includes(value.toLowerCase()))
                        .length;
                    __accumulateScore(matches, totalScore);
                }
            };

            const __processFileUpload = (message) => {
                const { blockRef, content, text } = message;
                const input = !content.skipped ? '&FILE_UPLOAD&' : text;
                __collectData(
                    blockRef[flowAttributes.ID],
                    blockRef[flowAttributes.CONTENT][flowAttributes.CONTENT_TEXT],
                    input,
                    blockRef[flowAttributes.DATA_TYPE],
                    input.trim().split(' ').filter(n => n),
                    content.skipped,
                    { fileName: content.fileName });

                if (!content.skipped)
                    submittedFiles = submittedFiles.concat({
                        file: content.file,
                        uploadedFileName: content.file.name,
                        fileName: content.fileName,
                        key: blockRef.DataType.enumName
                    });
            };

            const __processSolutions = (message) => {
                const { blockRef, content, text } = message;
                const solutions = !content.skipped ? content.selectedSolutions : [];
                __collectData(
                    blockRef[flowAttributes.ID],
                    'Database scanning',
                    solutions.length > 0 ? `Selected ${solutions.length} solution(s)` : text,
                    blockRef[flowAttributes.DATA_TYPE],
                    [],
                    content.skipped);
                if (solutions.length) {
                    __recordUserTypes(solutions[0][solutionAttributes.DATABASE_TYPE][solutionAttributes.DATABASE_TYPE_USER_TYPES]);
                    selectedSolutions = selectedSolutions.concat(solutions);
                }
            };

            const __processSalaryPicker = (message) => {
                const { blockRef, content, text } = message;
                const { input, skipped } = content;

                __collectData(
                    blockRef[flowAttributes.ID],
                    blockRef[flowAttributes.CONTENT][flowAttributes.CONTENT_TEXT],
                    input,
                    blockRef[flowAttributes.DATA_TYPE],
                    [input],
                    skipped);
            };

            const __processDatePicker = (message) => {
                const { blockRef, content, text } = message;
                const { input, skipped } = content;

                __collectData(
                    blockRef[flowAttributes.ID],
                    blockRef[flowAttributes.CONTENT][flowAttributes.CONTENT_TEXT],
                    input,
                    blockRef[flowAttributes.DATA_TYPE],
                    input.split(','),
                    skipped);
            };

            const __getResult = () => {
                userType = userType === 'Unknown' ? __detectUserType() : userType;
                let name, email, phone;
                if (userType === 'Candidate') {
                    name = personalData.CandidateName;
                    email = personalData.CandidateEmail;
                    phone = personalData.CandidateMobile;
                }
                if (userType === 'Client') {
                    name = personalData.ClientName;
                    email = personalData.ClientEmail;
                    phone = personalData.ClientTelephone;
                }

                return {
                    collectedData: collectedData,
                    keywords: collectedKeywords,
                    solutionsReturned: fetchedSolutions.length,
                    selectedSolutions: selectedSolutions,
                    submittedFiles: submittedFiles,
                    userType: userType,
                    keywordsByDataType: keywordsByDataType,
                    isConversationCompleted: completed,
                    score: completed && _totalScore > 0 ? _curScore / _totalScore : 0.05,
                    timeSpent: Math.floor(timeElapsed / 1000),
                    hasFiles: submittedFiles.length > 0,
                    name: name || null,
                    email: email || null,
                    phone: phone || null
                };
            };
            // debugger;
            // process messages using the above private functions
            let message;
            for (message of messages) {
                if (message.sender === 'USER') {
                    const { blockRef } = message;
                    // const storeInDB = blockRef[flowAttributes.STORE_IN_DB];
                    __recordUserTypes(blockRef[flowAttributes.DATA_TYPE][flowAttributes.DATA_TYPE_USER_TYPES]);

                    switch (blockRef[flowAttributes.TYPE]) {
                        case messageTypes.QUESTION:
                            __processQuestion(message);
                            break;
                        case messageTypes.USER_INPUT:
                            __processUserInput(message);
                            break;
                        case messageTypes.FILE_UPLOAD:
                            __processFileUpload(message);
                            break;
                        case messageTypes.SOLUTIONS:
                            __processSolutions(message);
                            break;
                        case messageTypes.SALARY_PICKER:
                            __processSalaryPicker(message);
                            break;
                        case messageTypes.DATE_PICKER:
                            __processDatePicker(message);
                            break;

                        case messageTypes.USER_TYPE:
                        case messageTypes.JOB_TYPE:
                            __processPredefinedAnswers(message);
                            break;
                        default:
                    }
                }
            }

            return __getResult(completed);
        };

        return {
            setAssistantID,
            setSessionID,
            sendData,
            processMessages,
            updateMessages,
            fetchSolutions,
            incrementTimeElapsed,
            resetTimeElapsed,
            cancelRequest
        };
    };

    if (!instance) {
        instance = init();
    }
    return { ...instance };
})();

