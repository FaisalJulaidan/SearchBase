import {delay} from 'redux-saga'
import {put, takeEvery, all} from 'redux-saga/effects'

const fetchAssistantsSaga = () => {
    return 'done'
};

// Our worker Saga: will perform the async increment task
function* incrementAsync() {
    yield delay(1000)
    yield put({type: 'INCREMENT'})
}

// Our watcher Saga: spawn a new incrementAsync task on each INCREMENT_ASYNC
function* watchIncrementAsync() {
    yield takeEvery('INCREMENT_ASYNC', incrementAsync)
}


// notice how we now only export the rootSaga
// single entry point to start all Sagas at once
export function* assistantSaga() {
    yield all([
        watchIncrementAsync()
    ])
}