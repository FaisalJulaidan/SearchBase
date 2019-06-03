import {createStore, applyMiddleware, compose} from 'redux';
import thunk from 'redux-thunk'
import createSagaMiddleware from 'redux-saga';
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import rootReducer from './reducers';
import { middleware as thunkMiddleware } from 'redux-saga-thunk'
import {
    assistantSaga,
    authSaga,
    profileSaga,
    conversationSaga,
    usersManagementSaga,
    databaseSaga,
    optionsSaga,
    crmSaga,
    autoPilotSaga
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
    composeEnhancers(applyMiddleware(thunkMiddleware, sagaMiddleware))
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
sagaMiddleware.run(autoPilotSaga);


export { store, persistor }

