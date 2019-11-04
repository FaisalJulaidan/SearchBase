import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {account} from "./account.reducer";
import {conversation} from "./conversation.reducer";
import {usersManagement} from "./usersManagement.reducer";
import {database} from "./database.reducer";
import {options} from "./options.reducer";
import {marketplace} from "./marketplace.reducer";
import {analytics} from './analytics.reducer'
import {autoPilot} from "./autoPilot.reducer";
import {appointmentsPicker} from "./appointmentsPicker.reducer";
import {appointment} from "./appointment.reducer";
import {appointmentAllocationTime} from "./appointmentAllocationTime.reducer";
import {development} from "./development.reducer";
import {campaign} from "./campaign.reducer";
import {payment} from "./payment.reducer";

import * as actionTypes from '../actions/actionTypes';
import storage from 'redux-persist/lib/storage'


const appReducer = combineReducers({
    auth,
    marketplace,
    assistant,
    autoPilot,
    account,
    conversation,
    usersManagement,
    database,
    options,
    analytics,
    appointmentsPicker,
    appointment,
    appointmentAllocationTime,
    development,
    campaign,
    payment
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
