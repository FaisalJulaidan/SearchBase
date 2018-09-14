
var assistant = null;
var blocks = []; // Blocks ordered
var currentBlock = undefined
var keywords = [];
var cancelScroll = false;
var chatInputDiv = document.getElementById("ChatInputDiv");

//old vars need check if needed
var oldPos = 0;
var newPos = 0;
var params = "";
var questionsAnswered = 0;
var collectedInformation = [];


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
    // 1.Show the chatbot welcoming message assistant.message

    // 2.Show the first block in the blocks array then render it depends on its type
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
    $("#qAnswers").remove();
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
function renderQuestion(block) {
    var answerAppendString = "<div id='qAnswers'>";
    document.getElementById("textMessage").style.display = "inline-block";
    document.getElementById("fileUploadDiv").style.display = "none";

    var blockAnswers = block.content.answers;
    for (var i = 1; i < blockAnswers.length; i++) {
        answerAppendString += "<a class='answerOptions' id='option" + i + "' onclick=\"submitAnswer('" + toEmoticon(blockAnswers[i].content.text) + "'," + blockAnswers[i].keywords + ")\">" + toEmoticon(blockAnswers[i].content.text) + "</a>";
    }
    //add skip button
    //answerAppendString += "<a class='answerOptions' id='option" + i + "' onclick=\"SkipQuestion()\">Skip Question</a>";
    answerAppendString += "</div>"
    $("#optionsDiv").append(answerAppendString);
    chatInputDiv.style = "display:none";

    sendAssistantMessage(block.text, 0)

    checkOutsideElements();
    if (!cancelScroll) {
        scrollTo("chatBottom");
    }
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

function submitAnswer(message, blockKeywords) {
    cancelScroll = false;

    if (currentBlock.type == "File Upload") {
        //needs rework
        //message = document.getElementById("fileUploadB").value.split("\\")[document.getElementById("fileUploadB").value.split("\\").length - 1];
        //fileUploads.push(currentFileURL + ":::" + questionID + ":::" + message);
    }

    if (message == "") { //been submited through Send button click
        message = document.getElementById("textMessage").value;
        if (message == "" || message.replace(/ /g, "") == "") {
            return 0;
        }
        $('#textMessage').val("");
    }

    $("#qAnswers").remove();
    chatInputDiv.style = "display:none";
    
    sendUserMessage(message, 500) //print user's message in the chatbox to appear like he is typing back
    
    putThinkingGif(900);

    if (currentBlock.storeInDB) {
        if (currentBlock.type != "UserInput") {
            collectedInformation.push({ "blockID": currentBlock.id, "input": message, "keywords": blockKeywords });
        } else {
            collectedInformation.push({ "blockID": currentBlock.id, "input": message, "keywords": [] });
        }

        sendAssistantMessage(generateUserInputThanks(), 300)

        putThinkingGif(500);
    }

    addKeywords(blockKeywords)

    getNextBlock();
}

function getNextBlock() {
    var targetBlock = undefined
    if (currentBlock.action == "Go To Next Block") {
        var blockNumber = currentBlock.order + 1;
        targetBlock = blocks[blockNumber];
    }
    else if (currentBlock.action == "Go To Specific Block") {
        for (var i = 0; i < blocks.length; i++) {
            if (blocks[i].id == currentBlock.blockToGoID) { targetBlock = blocks[i]; }
        }
    }
    else if (currentBlock.action == "Show Solutions") {
        //send the request to server
        return 0;
    }

    if (currentBlock != undefined) {
        if (currentBlock != targetBlock) {
            renderBlock(targetBlock);
        }
    }
}

function SetRepeat() {
    $("#optionsDiv").append("<div style='text-align: center;' onclick=\"Reset()\" id='qAnswers'><a class='answerOptions' style='width:400px;'>Search Again</a></div>");
    checkOutsideElements();
}

function Reset() {
    cancelScroll = false;
    $("#qAnswers").remove();
    keywords = [];
    collectedInformation = [];
    questionsAnswered = 0;
    start();
}


// helper functions
function sendUserMessage(message, waitTime) {
    $("#messagesContainer").append("<div class='ucDiv'><li id='newMessage' class='userChat'>" + toEmoticon(message) + "</li></div>");
    animateMessage("#newMessage");
    document.getElementById('newMessage').id = 'oldMessage';
    await sleep(waitTime);
}

function sendAssistantMessage(message, waitTime) {
    $("#messagesContainer").append("<div class='tsbDiv'><li id='newMessage' class='TSBbot'>" + toEmoticon(message) + "</li></div>");
    animateMessage("#newMessage");
    document.getElementById('newMessage').id = 'oldMessage';
    await sleep(waitTime);
}

function putThinkingGif(addMiliseconds) {
    $("#messagesContainer").append("<div class='tsbDiv'><li class='TSBbot' id='thinkingGif'><img src='/static/images/typing.gif'></li></div>")
    animateMessage("#thinkingGif");
    await sleep(400 + Math.floor(Math.random() * addMiliseconds));
    $("#thinkingGif").remove();
}

function addKeywords(blockKeywords) {
    var addIn = true;

    for (var c = 0; c < blockKeywords.length; c++) {
        addIn = true;

        for (var i = 0; i < keywords.length; i++) {
            if (blockKeywords[c] == keywords[i]) {
                addIn = false;
                break;
            }
        }

        if (addIn) { keywords.push(blockKeywords[c]); }
    }
}

function generateUserInputThanks() {
    var thanks = "";
    switch (Math.round(Math.random() * 6)) {
        case 0:
            thanks = "Thanks 😁";
            break;
        case 1:
            thanks = "Thank you 😃";
            break;
        case 2:
            thanks = "I'll remember that 😉";
            break;
        case 3:
            thanks = "Just one of the things that make you cool 😎";
            break;
        case 4:
            thanks = "Let me just write it down ✍️😊";
            break;
        case 5:
            thanks = "Give me a second to operate that information 😷";
            break;
        case 6:
            thanks = "Thanks 👊";
            break;
    }
    return thanks
}

function animateMessage(id) {
    var marginAnimate = "-=25px";
    if (id == "#thinkingGif") { marginAnimate = "-=25px"; }
    else if (id == "#newMessage") { marginAnimate = "-=35px"; }
    $(id).animate({
        marginTop: marginAnimate
    }, "slow");
    if (!cancelScroll) {
        scrollTo("chatBottom");
    }
}

function toEmoticon(message) {
    return emojione.toImage(message);
}