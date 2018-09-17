
var assistant = null;
var blocks = []; // Blocks ordered
var currentBlock = undefined;
var keywords = [];
var cancelScroll = false;
var chatInputDiv = document.getElementById("ChatInputDiv");
var oldPos = 0;
var newPos = 0;
var collectedInformation = [];
var fileUpload = false;
var params = undefined;

//scrolling setter
$(window).scroll(function () {
    newPos = $(window).scrollTop();
    if (newPos + 3 < oldPos) {
        $('html, body').stop();
        cancelScroll = true;
    }
    oldPos = newPos;
});
jQuery.expr.filters.offscreen = function (el) {
    var rect = el.getBoundingClientRect();
    return (
        (rect.x + rect.width) > window.innerWidth
    );
};

// This function will get the blocks from the server by assistantID and set the blocks array to be used to create
// the cahtbot conversational flow
function chatbotInit(assistantID) {
    console.log("Chatbot Init...");
     $.ajax({
        url: '../assistant/' + assistantID +'/chatbot',
        type: "GET"
    }).done(function (res) {

        console.log("Blocks retrieved successfully!");
        var data = JSON.parse(res).data;

        // Set assistant and blocks array
        assistant = data.assistant;
        blocks = data.blocks;

        // Start the chatbot
        //console.log(blocks)
        start();

        // Test
        //console.log(blocks);
        //console.log(assistant.name);

    }).fail(function (res) {
        console.log("Error in retrieving blocks.");
        console.log(res);
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
        if (blocks[i].id === id) {
            return blocks[i]
        }
    }
    // If nothing found return null
    return null
}

// This should send the data to the server, data such as keywords and inputs.
// and get  the solutions back based on the sent data
function sendData(){
    var solutions = [];
    params = {"collectedInformation": collectedInformation, "keywords": keywords, "solutionsHighest": 5};
    console.log("Send data...");
    console.log(params);
    $.ajax({
        contentType: 'application/json', //this is important
        url: '../assistant/' + assistantID +'/chatbot', // We still don't have this
        type: "POST",
        data: JSON.stringify(params)

    }).done(function (res) {

        console.log("Solutions retrieved successfully!");
        var data = JSON.parse(res).data;
        solutions = data.solutions;

    }).fail(function (res) {
        console.log("Error in retrieving blocks.");
        console.log(res);
    });
    return solutions
}


function openSolution(link) {
    window.open(link);
}


// Blocks Renderer //
// --------------- //

function renderBlock(block) {
    $("#qAnswers").remove();
    currentBlock = block;

    switch (block.type) {
        case "Question":
            renderQuestion(block);
            break;
        case "User Input":
            renderUserInput(block);
            break;
        case "File Upload":
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
    for (var i = 0; i < blockAnswers.length; i++) {
        answerAppendString += "<a class='answerOptions' id='option" + i + "' onclick=\"submitAnswer('" + toEmoticon(blockAnswers[i].answer.text) + "','" + blockAnswers[i].keywords + "')\">" + toEmoticon(blockAnswers[i].answer.text) + "</a>";
    }
    //add skip button
    //answerAppendString += "<a class='answerOptions' id='option" + i + "' onclick=\"SkipQuestion()\">Skip Question</a>";
    answerAppendString += "</div>"
    $("#optionsDiv").append(answerAppendString);
    chatInputDiv.style = "display:none";
    
    sendAssistantMessage(block.content.text)

    checkOutsideElements();
    if (!cancelScroll) {
        scrollTo("chatBottom");
    }
}

function renderUserInput(block) {
    // make sure to validate user's input depends on block.content.validation
    document.getElementById("textMessage").style.display = "inline-block";
    document.getElementById("fileUploadDiv").style.display = "none";
    chatInputDiv.style = "display:block";

    sendAssistantMessage(block.content.text)
}

function renderFileUpload(block) {
    document.getElementById("textMessage").style.display = "none";
    document.getElementById("fileUploadDiv").style.display = "inline-block";
    chatInputDiv.style = "display:block";

    sendAssistantMessage(block.content.text)
}

function renderSolutions(block) {
    //Abdullah still did not finish a block of type solutions
    // However reaching to this block means you have to sendData() and get the solutions back
}

async function submitAnswer(message, blockKeywords=undefined) {
    cancelScroll = false;

    if (currentBlock.type == "File Upload") {
        //needs rework
        message = document.getElementById("fileUploadB").value.split("\\")[document.getElementById("fileUploadB").value.split("\\").length - 1];
        if (!checkFileFormat(message)) {
            sendUserMessage(message)
            await sleep(350);
            sendAssistantMessage("That did not match the allowed file types I've been given. They are " + getAllowedFormatsString() + ".")
            return 0;
        }
        //fileUploads.push(currentFileURL + ":::" + questionID + ":::" + message);
    }

    if (message == "") { //been submited through Send button click
        message = document.getElementById("textMessage").value;
        if (message == "" || message.replace(/ /g, "") == "") {
            return 0;
        }
        $('#textMessage').val("");
    }
    
    if (currentBlock.type == "User Input") { //validate user input
        if (!validateUserInput(message, currentBlock.content.validation)) {
            sendUserMessage(message)
            await sleep(350);
            sendAssistantMessage("I am sorry but that was not in the format I think it should be...")
            return 0;
        }
    }

    $("#qAnswers").remove();
    chatInputDiv.style = "display:none";
    
    sendUserMessage(message) //print user's message in the chatbox to appear like he is typing back
    await sleep(500);
    
    putThinkingGif();
    await sleep(400 + Math.floor(Math.random() * 900));
    removeThinkingGif();

    if (currentBlock.storeInDB) {
        if (currentBlock.type == "Question" && blockKeywords !== undefined) {
            blockKeywords = blockKeywords.split(",");
            collectedInformation.push({ "blockID": currentBlock.id, "QuestionText": currentBlock.content.text, "input": message, "keywords": blockKeywords });
            addKeywords(blockKeywords)
        } else {
            collectedInformation.push({ "blockID": currentBlock.id, "QuestionText": currentBlock.content.text, "input": message, "keywords": [] });
        }

        sendAssistantMessage(generateUserInputThanks())
        await sleep(300);

        putThinkingGif();
        await sleep(400 + Math.floor(Math.random() * 500));
        removeThinkingGif();
    }

    var action = undefined;
    if (currentBlock.type == "Question") {
        var blockAnswers = currentBlock.content.answers;
        for (var i = 0; i < blockAnswers.length; i++) {
            if (blockAnswers[i].keywords.equals(blockKeywords) && blockAnswers[i].answer.text == message) {
                action = blockAnswers[i].action;
                var blockToGoId = blockAnswers[i].blockToGoId;

                getNextBlock(action, blockToGoId);
            }
        }
    } else if (currentBlock.type == "User Input" || currentBlock.type == "File Upload") {
        action = currentBlock.content.action;

        getNextBlock(action);
    }

}

function getNextBlock(action, blockToGoId=undefined) {
    var targetBlock = undefined

    if (action == "Go To Next Block") {
        targetBlock = blocks[currentBlock.order]; //order starts from 1 and array from 0 so it just needs the current .order
        if (targetBlock === undefined) {
            sendData()
            return 0;
        }
    }
    else if (action == "Go To Specific Block") {
        for (var i = 0; i < blocks.length; i++) {
            if (blocks[i].id == blockToGoId) {
                targetBlock = blocks[i];
            }
        }
    }
    else if (action == "Show Solutions") {
        sendData()
        return 0;
    }

    if (currentBlock != undefined) { //check if its not trying to reload the same block
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
    fileUpload = false;
    start();
}


// helper functions
function sendUserMessage(message) {
    $("#messagesContainer").append("<div class='ucDiv'><li id='newMessage' class='userChat'>" + toEmoticon(message) + "</li></div>");
    animateMessage("#newMessage");
    document.getElementById('newMessage').id = 'oldMessage';
}

function sendAssistantMessage(message) {
    $("#messagesContainer").append("<div class='tsbDiv'><li id='newMessage' class='TSBbot'>" + toEmoticon(message) + "</li></div>");
    animateMessage("#newMessage");
    document.getElementById('newMessage').id = 'oldMessage';
}

function putThinkingGif() {
    $("#messagesContainer").append("<div class='tsbDiv'><li class='TSBbot' id='thinkingGif'><img src='/static/images/typing.gif'></li></div>")
    animateMessage("#thinkingGif");
}

function removeThinkingGif() {
    $("#thinkingGif").remove();
}

function validateUserInput(message, messageType) {
    var emailRegex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    if (messageType == "Email" && !message.match(emailRegex)) {
        return false;
    } else if (messageType == "FullName" && name.indexOf(' ') <= 0) {
        return false;
    } else if (messageType == "Telephone" && !/^[0-9]*$/.test(message)) {
        return false;
    }

    return true;
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

function checkFileFormat(message) {
    var messageSplit = message.split(".");
    var format = messageSplit[messageSplit.length - 1];
    var allowedFormats = currentBlock.content.fileTypes;
    var passes = false;
    for (var i = 0; i < allowedFormats.length; i++) {
        if (allowedFormats[i] === format) {
            passes = true;
        }
    }
    return passes;
}

function getAllowedFormatsString() {
    var formats = "";
    var allowedFormats = currentBlock.content.fileTypes;
    for (var i = 0; i < allowedFormats.length; i++) {
        formats += allowedFormats[i] + ", ";
    }
    formats = formats.slice(0, -2);
    return formats;
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

function checkOutsideElements() {
    var offScreenElements = $(':offscreen');
    for (var z = 0; z < offScreenElements.length; z++) {
        var elementID = offScreenElements[z].outerHTML.split("id=\"")[1].split("\"")[0];
        $("<br><br>").insertBefore("#" + elementID);
        checkOutsideElements();
        return 0;
    }
}

function scrollTo(id) {
    $('html, body').stop();
    id = "#" + id
    $('html, body').animate({
        scrollTop: ($(id).offset().top)
    }, 2000);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function handleEnter(e) {
    var keycode = (e.keyCode ? e.keyCode : e.which);
    if (keycode == '13') {
        submitAnswer('');
    }
}

//compare arrays function
// Warn if overriding existing method
if (Array.prototype.equals)
    console.warn("Overriding existing Array.prototype.equals. Possible causes: New API defines the method, there's a framework conflict or you've got double inclusions in your code.");
// attach the .equals method to Array's prototype to call it on any array
Array.prototype.equals = function (array) {
    // if the other array is a falsy value, return
    if (!array)
        return false;

    // compare lengths - can save a lot of time 
    if (this.length != array.length)
        return false;

    for (var i = 0, l = this.length; i < l; i++) {
        // Check if we have nested arrays
        if (this[i] instanceof Array && array[i] instanceof Array) {
            // recurse into the nested arrays
            if (!this[i].equals(array[i]))
                return false;
        }
        else if (this[i] != array[i]) {
            // Warning - two different object instances will never be equal: {x:20} != {x:20}
            return false;
        }
    }
    return true;
}
// Hide method from for-in loops
Object.defineProperty(Array.prototype, "equals", { enumerable: false });