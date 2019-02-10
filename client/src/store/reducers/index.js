import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {flow} from "./flow.reducer";
import {profile} from "./profile.reducer";
import {chatbotSessions} from "./chatbotSessions.reducer";
import {solutions} from "./solutions.reducer";
import {usersManagement} from "./usersManagement.reducer";
import {database} from "./database.reducer";


const rootReducer = combineReducers({
    auth,
    assistant,
    flow,
    profile,
    chatbotSessions,
    solutions,
    usersManagement,
    database
});

export default rootReducer;