import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {profile} from "./profile.reducer";
import {conversation} from "./conversation.reducer";
import {usersManagement} from "./usersManagement.reducer";
import {database} from "./database.reducer";
import {options} from "./options.reducer";
import {crm} from "./crm.reducer";
import {analytics} from './analytics.reducer'
import {autoPilot} from "./autoPilot.reducer";
import {appointmentsPicker} from "./appointmentsPicker.reducer";
import * as actionTypes from '../actions/actionTypes';
import storage from 'redux-persist/lib/storage'


const appReducer = combineReducers({
    auth,
    crm,
    assistant,
    autoPilot,
    profile,
    conversation,
    usersManagement,
    database,
    options,
    analytics,
    appointmentsPicker
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
