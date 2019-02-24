import {createStore, applyMiddleware, compose} from 'redux';
import createSagaMiddleware from 'redux-saga';
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
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
const persistConfig = {
    key: 'root',
    storage,
};
const persistedReducer = persistReducer(persistConfig, rootReducer);


const store = createStore(
    persistedReducer,
    composeEnhancers(applyMiddleware(sagaMiddleware))
);
const persistor = persistStore(store);


sagaMiddleware.run(assistantSaga);
sagaMiddleware.run(authSaga);
sagaMiddleware.run(profileSaga);
sagaMiddleware.run(chatbotSessions);
sagaMiddleware.run(solutionsSaga);
sagaMiddleware.run(usersManagementSaga);
sagaMiddleware.run(databaseSaga);
sagaMiddleware.run(optionsSaga);

export { store, persistor }

