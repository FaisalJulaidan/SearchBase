import {createStore, applyMiddleware, compose} from 'redux';
import createSagaMiddleware from 'redux-saga';
import rootReducer from './reducers';
import {
    assistantSaga,
    authSaga,
    profileSaga,
    chatbotSessions,
    solutionsSaga,
    usersManagementSaga,
    databaseSaga,
    optionsSaga
} from './sagas'

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const sagaMiddleware = createSagaMiddleware();

const store = createStore(
    rootReducer,
    composeEnhancers(applyMiddleware(sagaMiddleware))
);

sagaMiddleware.run(assistantSaga);
sagaMiddleware.run(authSaga);
sagaMiddleware.run(profileSaga);
sagaMiddleware.run(chatbotSessions);
sagaMiddleware.run(solutionsSaga);
sagaMiddleware.run(usersManagementSaga);
sagaMiddleware.run(databaseSaga);
sagaMiddleware.run(optionsSaga);


export default store;