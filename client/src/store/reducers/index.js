import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {flow} from "./flow.reducer";
import {profile} from "./profile.reducer";
import {chatbotSessions} from "./chatbotSessions.reducer";
import {solutions} from "./solutions.reducer";


const rootReducer = combineReducers({
    auth,
    assistant,
    flow,
    profile,
    chatbotSessions,
    solutions
});

export default rootReducer;