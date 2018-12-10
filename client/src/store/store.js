import {createStore, applyMiddleware, compose} from 'redux';
import createSagaMiddleware from 'redux-saga';
import rootReducer from './reducers';
import {assistantSaga, authSaga, flowSaga, settingsSage} from './sagas'

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const sagaMiddleware = createSagaMiddleware();

const store = createStore(
    rootReducer,
    composeEnhancers(applyMiddleware(sagaMiddleware))
);

sagaMiddleware.run(flowSaga);
sagaMiddleware.run(assistantSaga);
sagaMiddleware.run(authSaga);
sagaMiddleware.run(settingsSage);


export default store;