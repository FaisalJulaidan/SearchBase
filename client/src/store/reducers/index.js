import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {assistant} from "./assistant.reducer";



const rootReducer = combineReducers({
    auth,
    assistant
});

export default rootReducer;