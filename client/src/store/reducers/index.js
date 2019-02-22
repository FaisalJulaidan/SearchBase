import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {profile} from "./profile.reducer";
import {chatbotSessions} from "./chatbotSessions.reducer";
import {solutions} from "./solutions.reducer";
import {usersManagement} from "./usersManagement.reducer";
import {database} from "./database.reducer";
import {options} from "./options.reducer";


const rootReducer = combineReducers({
    auth,
    assistant,
    profile,
    chatbotSessions,
    solutions,
    usersManagement,
    database,
    options,
});

export default rootReducer;