
var assistant = null;
var blocks = []; // Blocks ordered
var keywords = [];


// This function will get the blocks from the server by assistantID and set the blocks array to be used to create
// the cahtbot conversational flow
function chatbotInit(assistantID) {
    console.log("Chatbot Init...");
     $.ajax({
        url: 'assistant/' + assistantID +'/chatbot',
        type: "GET"
    }).done(function (res) {

        console.log("Blocks retrieved successfully!");
        var data = JSON.parse(res).data;

        // Set assistant and blocks array
        assistant = data.assistant;
        blocks = data.blocks;

        // Start the chatbot
        start();

        // Test
        console.log(blocks);
        console.log(assistant.name);

    }).fail(function (res) {
        console.log("Error in retrieving blocks.");
        console.log(res);
    });
}


function f() {
      $.ajax({
          url: '/test',
          contentType: 'application/json', //this is important
          type: "POST",
          data: JSON.stringify({"keywords": ["smoker","anger"]})
    }).done(function (res) {
        console.log("GOOD");
    }).fail(function (res) {
        console.log("Error");
    });
}




// This start the lunch the chatbot for the first time
function start() {
    // 1.Popup the chatbot after assistant.secondsUntilPopup

    // 2.Show the chatbot welcoming message assistant.message

    // 3.Show the first block in the blocks array then render it depends on its type
    renderBlock(blocks[0]);
}


// Get block by id
function getBlock(id) {
    for (var i = 0, l = blocks.length; i < l; i++) {
        if(blocks[i].id === id){
            return blocks[i]
        }
    }
    // If nothing found return null
    return null
}


// This function what manages the flow of the chatbot conversation depends on the user's interaction with the chatbot.
function submitMessage() {

}

// This should send the data to the server, data such as keywords.
// and get  the solutions back based on the sent data
function sendData(){
    var solutions = [];
    var dataToSend = null;
     console.log("Send data...");
     $.ajax({
        url: 'assistant/' + assistantID +'/solutions', // We still don't have this
        type: "GET",
        data: dataToSend
    }).done(function (res) {

        console.log("Solutions retrieved successfully!");
        var data = JSON.parse(res).data;

    }).fail(function (res) {
        console.log("Error in retrieving blocks.");
        console.log(res);
    });
    return solutions
}


function openSolution(link) {
    window.open(link);
}

function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
}


// Blocks Renderer //
// --------------- //

function renderBlock(block) {
    switch (block.type) {
        case "Question":
            renderQuestion(block);
            break;
        case "UserInput":
            renderUserInput(block);
            break;
        case "FileUpload":
            renderFileUpload(block);
            break;
        case "Solutions":
            renderSolutions(block);
            break;
        default:
            console.log("Block type is not recognised!!!")
    }
}

// This function will render a block of type Questions with its answers to the chatbot.
// not finished but just to give an idea of what should be done inside this function
function renderQuestion(block) {
    return "<div data-block-id='" + block.id +"' data-block-type='Question'>" + block.content.text +
        "<div>"+ block.content.answers + "</div>"+
        "</div>"
}

function renderUserInput(block) {
    // make sure to validate user's input depends on block.content.validation
}

function renderFileUpload(block) {

}

function renderSolutions(block) {
    //Abdullah still did not finish a block of type solutions
    // However reaching to this block means you have to sendData() and get the solutions back
}