import {applyMiddleware, compose, createStore} from 'redux';
import createSagaMiddleware from 'redux-saga';
import {persistReducer, persistStore} from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import rootReducer from './reducers';
import {middleware as thunkMiddleware} from 'redux-saga-thunk'
import {
    analyticsSaga,
    appointmentsPickerSaga,
    assistantSaga,
    authSaga,
    autoPilotSaga,
    conversationSaga,
    marketplaceSaga,
    databaseSaga,
    optionsSaga,
    accountSaga,
    usersManagementSaga,
    appointmentAllocationTimeSaga,
    developmentSaga,
    appointmentSaga,
    campaignSaga,
    paymentSaga
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
sagaMiddleware.run(accountSaga);
sagaMiddleware.run(conversationSaga);
sagaMiddleware.run(usersManagementSaga);
sagaMiddleware.run(databaseSaga);
sagaMiddleware.run(optionsSaga);
sagaMiddleware.run(marketplaceSaga);
sagaMiddleware.run(autoPilotSaga);
sagaMiddleware.run(analyticsSaga);
sagaMiddleware.run(appointmentsPickerSaga);
sagaMiddleware.run(appointmentSaga);
sagaMiddleware.run(appointmentAllocationTimeSaga);
sagaMiddleware.run(developmentSaga);
sagaMiddleware.run(campaignSaga);
sagaMiddleware.run(paymentSaga);


export { store, persistor }

