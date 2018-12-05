import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";
import {flow} from "./flow.reducer";


const rootReducer = combineReducers({
    auth,
    assistant,
    flow
});

export default rootReducer;