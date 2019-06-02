import {createStore, applyMiddleware, compose} from 'redux';
import createSagaMiddleware from 'redux-saga';
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import rootReducer from './reducers';
import {
    assistantSaga,
    analyticsSaga,
    authSaga,
    profileSaga,
    conversationSaga,
    usersManagementSaga,
    databaseSaga,
    optionsSaga,
    crmSaga
} from './sagas'

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const sagaMiddleware = createSagaMiddleware();
const persistConfig = {
    key: 'root',
    storage,
    blacklist: ['auth', 'database']
};


const persistedReducer = persistReducer(persistConfig, rootReducer);


const store = createStore(
    persistedReducer,
    // { ...authActions.checkAuthTimeout(), ...window.__PRELOADED_STATE__ },
    composeEnhancers(applyMiddleware(sagaMiddleware))

);
const persistor = persistStore(store);

sagaMiddleware.run(assistantSaga);
sagaMiddleware.run(authSaga);
sagaMiddleware.run(profileSaga);
sagaMiddleware.run(conversationSaga);
sagaMiddleware.run(usersManagementSaga);
sagaMiddleware.run(databaseSaga);
sagaMiddleware.run(optionsSaga);
sagaMiddleware.run(crmSaga);
sagaMiddleware.run(analyticsSaga);


export { store, persistor }

