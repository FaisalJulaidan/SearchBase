#!/usr/bin/env node

const inquirer = require("inquirer");
const chalk = require("chalk");
const figlet = require("figlet");
const shell = require("shelljs");


const init = () => {
    console.log(
        chalk.green(
            figlet.textSync("SAGA GENERATOR", {
                horizontalLayout: "default",
                verticalLayout: "default"
            })
        )
    );
};

const askQuestions = () => {
    const questions = [
        {
            name: "SAGA_NAME",
            type: "input",
            message: "Enter the name of the saga endpoint should be separted"
        },
        {
            name: "ACTION_NAME",
            type: "input",
            message: "Enter name of action - click enter to use default value"
        }
    ];
    return inquirer.prompt(questions);
};


const createActionTypes = (sagaName) => {
    const placeholder = sagaName.toUpperCase().split(' ').join('_');
    return `
    COPY AND PASTE THIS IN actionTypes.js file:
    
     export const ${placeholder}_REQUEST = '${placeholder}_REQUEST';
     export const ${placeholder}_SUCCESS = '${placeholder}_SUCCESS';
     export const ${placeholder}_FAILURE = '${placeholder}_FAILURE';
     
==================== 
    `;
};

function camelize(str) {
    return str.replace(/(?:^\w|[A-Z]|\b\w)/g, function (word, index) {
        return index === 0 ? word.toLowerCase() : word.toUpperCase();
    }).replace(/\s+/g, '');
}

function PascalCase(string) {
    return `${string}`
        .replace(new RegExp(/[-_]+/, 'g'), ' ')
        .replace(new RegExp(/[^\w\s]/, 'g'), '')
        .replace(
            new RegExp(/\s+(.)(\w+)/, 'g'),
            ($1, $2, $3) => `${$2.toUpperCase() + $3.toLowerCase()}`
        )
        .replace(new RegExp(/\s/, 'g'), '')
        .replace(new RegExp(/\w/), s => s.toUpperCase());
}

const createActions = (sagaName) => {
    const placeholder_camel = camelize(sagaName);
    const placeholder_Upper = sagaName.toUpperCase().split(' ').join('_');
    return `COPY AND PASTE THIS IN .actions.js file:
    
    const ${placeholder_camel} = () => {
        return {
            type: actionTypes.${placeholder_Upper}_REQUEST,
        };
    };

    const ${placeholder_camel}Success = (msg) => {
        return {
            type: actionTypes.${placeholder_Upper}_SUCCESS,
            msg
        };
    };

    const ${placeholder_camel}Failure = (error) => {
        return {
            type: actionTypes.${placeholder_Upper}_FAILURE,
            error
        };
    };
    
    COPY AND PASTE THIS IN EXPORT FUNCTION:
    ${placeholder_camel},
    ${placeholder_camel}Success,
    ${placeholder_camel}Failure,
    
====================  
    `;
};

const createReducer = (sagaName) => {
    const placeholder_Upper = sagaName.toUpperCase().split(' ').join('_');

    return `COPY AND PASTE THIS IN .reducer.js file:
    
    case actionTypes.${placeholder_Upper}_REQUEST:
        return updateObject(state, {
            errorMsg: null,
        });
    case actionTypes.${placeholder_Upper}_SUCCESS:
        return updateObject(state, {
        });
    case actionTypes.${placeholder_Upper}_FAILURE:
        return updateObject(state, {
            errorMsg: action.error
        });
    
====================  
    `;
};

const createSaga = (sagaName, actionName) => {
    const placeholder_camel = camelize(sagaName);
    const placeholder_pascal = PascalCase(sagaName);
    const placeholder_Upper = sagaName.toUpperCase().split(' ').join('_');
    const actionFile = actionName.trim() ? actionName : 'IMPORT_ACTIONS';

    return `COPY AND PASTE THIS IN .saga.js file:
    
    function* ${placeholder_camel}(payload) {
        const defaultMsg = "CHANGE THIS";
        try {
            // TODO: CHANGE THE HTTP TYPE & API NAME & PAYLOAD 
            const res = yield http.post('TODO', {});
            successMessage(res.data?.msg || defaultMsg);
            yield put(${actionFile}.${placeholder_camel}Success());
        } catch (error) {
            let data = error.response?.data;
            errorMessage(data.msg || defaultMsg);
            yield put(${actionFile}.${placeholder_camel}Failure(data.msg || defaultMsg));
            if (!data.msg) errorHandler(error)
        }
    }

    function* watch${placeholder_pascal}() {
        yield takeEvery(actionTypes.${placeholder_Upper}_REQUEST, ${placeholder_camel})
    }
    
    
    //TODO: ADD THIS TO WATCHER FUNCTIONS
    watch${placeholder_pascal}()
      
    `;
};

const run = async () => {
    // show script introduction
    init();
    const answers = await askQuestions();

    const {SAGA_NAME, ACTION_NAME} = answers;

    const actionTypes = createActionTypes(SAGA_NAME);
    console.log(actionTypes);

    const actions = createActions(SAGA_NAME);
    console.log(actions);

    const reducer = createReducer(SAGA_NAME);
    console.log(reducer);

    const saga = createSaga(SAGA_NAME, ACTION_NAME);
    console.log(saga)


};

run();


