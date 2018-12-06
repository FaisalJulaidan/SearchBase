import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {flow} from "./flow.reducer";
import {settings} from "./settings.reducer";


const rootReducer = combineReducers({
    auth,
    assistant,
    flow,
    settings
});

export default rootReducer;