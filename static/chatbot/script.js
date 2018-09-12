
var  assistantID = 1;
// Blocks ordered
var blocks = [];



function chatbotInit() {
    console.log("Chatbot Init...");
     $.ajax({
        url: 'assistant/' + assistantID +'/chatbot',
        type: "GET"
    }).done(function (res) {

        console.log("Blocks retrieved successfully!");
        // Set blocks array
        blocks = JSON.parse(res).data;
        // Test
        console.log(blocks);

    }).fail(function (res) {
        console.log("Error in retrieving blocks.");
        console.log(res);
    });
}

function controller() {

}


function getNextBlock() {

}

function renderQuestion(block) {

}

function renderUserInput(block) {

}


function renderFileUpload(block) {

}

function renderSolutions(block) {

}