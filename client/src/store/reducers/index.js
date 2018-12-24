import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {flow} from "./flow.reducer";
import {settings} from "./assistantSettings.reducer";
import {profile} from "./profile.reducer";
import {userInput} from "./userInput.reducer";


const rootReducer = combineReducers({
    auth,
    assistant,
    flow,
    settings,
    profile,
    userInput
});

export default rootReducer;