import {createStore, applyMiddleware, compose} from 'redux';
import createSagaMiddleware from 'redux-saga';
import rootReducer from './reducers';
import {assistantSaga, authSaga, flowSaga} from './sagas'

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const sagaMiddleware = createSagaMiddleware();

const store = createStore(
    rootReducer,
    composeEnhancers(applyMiddleware(sagaMiddleware))
);

sagaMiddleware.run(flowSaga);
sagaMiddleware.run(assistantSaga);
sagaMiddleware.run(authSaga);


export default store;