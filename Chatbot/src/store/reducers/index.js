import messages from './messages';
import chatbot from './chatbot';
import { combineReducers } from 'redux';


export default combineReducers({ messages, chatbot });