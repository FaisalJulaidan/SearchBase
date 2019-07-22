import * as flowAttributes from '../constants/FlowAttributes';
import * as messageTypes from '../constants/MessageType';
import {dataHandler} from './dataHandler';
import {createBlock, delayMessageLength} from './';

const errorBlock = () => {
    // SEND SENTRY ERROR
    const text = 'Error occurred, sorry!';
    return createBlock({ text }, messageTypes.TEXT, delayMessageLength(text));
};

const notFoundBlock = (toGoID) => {
    // SEND SENTRY ERROR
    const text = 'Sorry, I could not find what you want!';
    return createBlock({ text }, messageTypes.TEXT, delayMessageLength(text), null, null, toGoID);
};

const endBlock = (finished=true) => {
    const text = 'This conversation has ended, if you would like to have a new one please click the reset button!';
    // Content, Type, delay, ID = null, DataType = null, selfContinue = null, extra = {})
    return createBlock(null, messageTypes.TEXT, 0, null, null, null, { end: true, finished });

};

const checkFetchData = (type) => {
    switch (type) {
        case messageTypes.SOLUTIONS:
            return { needsToFetch: true };
        default:
            return {};
    }
};

const checkSelfContinue = (type, blockToGoID) => {
    switch (type) {
        case messageTypes.RAW_TEXT:
            return blockToGoID ;
        default:
            return null;
    }
};

const loadNextBlock = (chatbot) => {
    try {
        const { curBlockID, finished } = chatbot.status;
        console.log(curBlockID)
        let potential = finished ? null : chatbot.blocks.find(block => block.ID === curBlockID);
        console.log(potential)
        let block = potential ? potential : null;
        if(!block) return endBlock();
        let extra = block.extra ? { ...block.extra, ...checkFetchData(block[flowAttributes.TYPE]) } : checkFetchData(block[flowAttributes.TYPE]);
        let selfContinue = checkSelfContinue(block[flowAttributes.TYPE], block[flowAttributes.CONTENT][flowAttributes.BLOCKTOGOID]);
        return { ...block, delay: delayMessageLength(block[flowAttributes.CONTENT][flowAttributes.TEXT]), selfContinue,  extra };

    } catch (e) {
      console.error(e)
    }
};

const loadAfterMessage = (chatbot) => {
    const { curBlock, curBlockID, afterMessage } = chatbot.status

    return createBlock(
        { text: afterMessage},
        messageTypes.TEXT,
        delayMessageLength(afterMessage),
        null,
        null,
        curBlockID
        )
}


const loadFirstBlock = (blocks) => {
    try {
        let extra = {};
        let block = blocks[0];
        return createBlock(
            block[flowAttributes.CONTENT],
            block[flowAttributes.TYPE],
            delayMessageLength(block[flowAttributes.CONTENT][flowAttributes.TEXT]),
            block[flowAttributes.ID]);
    } catch (e) {
    }
};

const fetchData = async (block) => {
    const { solutions, cancelled } = await dataHandler.fetchSolutions(block[flowAttributes.CONTENT][flowAttributes.SOLUTION_SHOW_TOP], block[flowAttributes.CONTENT][flowAttributes.SOLUTION_DATABASE_TYPE]);
    return ['solutions', solutions, cancelled];
};

const getCurBlock = (action, assistant, chatbot) => {
    const { blocks, status } = chatbot;
    const { curBlockID, afterMessage } = status;
    const { Message } = assistant;
    if(afterMessage){return  loadAfterMessage(chatbot)}
    /**
     * Batu please validate this:
     * Previously, if the action === null we end the chatbot
     * how we can do it now?
     * */
    switch (action) {
        case 'Init':
            return createBlock({ text: Message }, messageTypes.TEXT, delayMessageLength(Message), null, null, loadFirstBlock(blocks).ID);
        case 'Go To Next Block':
        case 'Go To Specific Block':
            return loadNextBlock(chatbot);
        case 'Early End Chat':
            return endBlock(false);
        case 'End Chat':
            return endBlock();
        case 'Not Found':
            return notFoundBlock(curBlockID);
        default:
            return null;
    }
};

export { getCurBlock, fetchData };

