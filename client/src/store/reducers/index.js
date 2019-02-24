import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {profile} from "./profile.reducer";
import {chatbotSessions} from "./chatbotSessions.reducer";
import {solutions} from "./solutions.reducer";
import {usersManagement} from "./usersManagement.reducer";
import {database} from "./database.reducer";
import {options} from "./options.reducer";
import * as actionTypes from '../actions/actionTypes';
import storage from 'redux-persist/lib/storage'




const appReducer = combineReducers({
    auth,
    assistant,
    profile,
    chatbotSessions,
    solutions,
    usersManagement,
    database,
    options,
});

const rootReducer = (state, action) => {
    if (action.type === actionTypes.LOGOUT) {
        Object.keys(state).forEach(key => {
            storage.removeItem(`persist:${key}`);
        });
        state = undefined
    }
    return appReducer(state, action)
};

export default rootReducer;