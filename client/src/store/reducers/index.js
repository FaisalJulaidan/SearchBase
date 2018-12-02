import {combineReducers} from 'redux';
import {auth} from './auth.reducer';
import {counter} from './counter.reducer';


const rootReducer = combineReducers({
    auth,
    counter
});

export default rootReducer;