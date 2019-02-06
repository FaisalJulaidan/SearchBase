import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {flow} from "./flow.reducer";
import {settings} from "./assistantSettings.reducer";
import {profile} from "./profile.reducer";
import {chatbotSessions} from "./chatbotSessions.reducer";
import {solutions} from "./solutions.reducer";
import {usersManagement} from "./usersManagement.reducer";


const rootReducer = combineReducers({
    auth,
    assistant,
    flow,
    settings,
    profile,
    chatbotSessions,
    solutions,
    usersManagement
});

export default rootReducer;