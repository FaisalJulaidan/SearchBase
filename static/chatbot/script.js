var assistant = null;
var blocks = []; // Blocks ordered
var currentBlock = undefined;
var keywords = [];
var cancelScroll = false;
var collectedInformation = [];
var fileUpload = false;
var params = undefined;
var sessionID = 0;
var welcomeMessage = "";
var BOT_USER = 'bot';
var CLIENT_USER = 'user';
var chatInputDiv = document.getElementById("message-input");
var fileUploadForm = document.getElementById('fileUploadForm');
var thinkingGifLife = 800 + Math.floor(Math.random() * 1200);

// This function will get the blocks from the server by assistantID and set the blocks array to be used to create
// the cahtbot conversational flow
function chatbotInit(assistantID) {
    console.log("Chatbot Init...");
    $.ajax({
        url: '../assistant/' + assistantID + '/chatbot',
        type: "GET"
    }).done(function (res) {

        console.log("Blocks retrieved successfully!");
        var data = JSON.parse(res).data;

        // Set assistant and blocks array
        assistant = data.assistant;
        blocks = data.blocks;
        welcomeMessage = assistant.message
        // Start the chatbot
        start();

    }).fail(function (res) {
        console.log("Error in retrieving blocks.");
        console.log(res);
    });
}


// This start the lunch the chatbot for the first time
async function start() {
    // 1.Show the chatbot welcoming message assistant.message
    if (welcomeMessage) {
        sendAssistantMessage(welcomeMessage);
    }

    await sleep(750)

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

// This should send the data to the server, without returning any solutions back
function sendData() {
    putThinkingGif();
    var solutions = [];
    params = {
        "collectedInformation": collectedInformation,
        "keywords": keywords,
        "showTop": 0,
        solutionsReturned: solutions.length
    };
    console.log("Send data...");

    return $.ajax({
        contentType: 'application/json', //this is important
        url: '../assistant/' + assistantID + '/chatbot',
        type: "POST",
        data: JSON.stringify(params)

    }).done(function (res) {
        removeThinkingGif();
        console.log("Data sent successfully!");
        var data = JSON.parse(res).data;
        sessionID = data["sessionID"];
        sendFile();
        return true;

    }).fail(function (res) {
        removeThinkingGif();
        console.log("Error in retrieving blocks.");
        console.log(res);
        return false
    });
}

function sendDataSolutionsBlock(showTop) {
    putThinkingGif();
    params = {"collectedInformation": collectedInformation, "keywords": keywords, "showTop": showTop};

    return $.ajax({
        contentType: 'application/json', //this is important
        url: '../assistant/' + assistantID + '/chatbot',
        type: "POST",
        data: JSON.stringify(params)

    }).done(function (res) {
        removeThinkingGif();

        console.log("Solutions retrieved successfully!");
        var data = JSON.parse(res).data;
        sessionID = data["sessionID"];
        solutions = data["solutions"];
        sendFile();
        return solutions;

    }).fail(function (res) {
        removeThinkingGif();
        console.log("Error in retrieving blocks.");
        console.log(res);
    });
}

function getSolutions(showTop) {
    putThinkingGif();
    params = {"keywords": keywords, "showTop": showTop};

    return $.ajax({
        contentType: 'application/json', //this is important
        url: '../assistant/' + assistantID + '/chatbot/solutions',
        type: "POST",
        data: JSON.stringify(params)

    }).done(function (res) {
        removeThinkingGif();

        console.log("Solutions retrieved successfully!");
        var data = JSON.parse(res).data;
        solutions = data["solutions"];
        return solutions;

    }).fail(function (res) {
        removeThinkingGif();
        console.log("Error in retrieving solutions.");
        console.log(res);
    });
}

function sendFile() {
    console.log("init form")
    sendFileForm();
}

function sendFileForm() {
    if (document.getElementById('fileUploadB').files.length == 0) {
        return false;
    }
    var formData = new FormData();
    var fileInput = document.getElementById('fileUploadB').files[0];
    formData.append('file', fileInput, fileInput.name);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', "../assistant/" + sessionID + "/file", true);

    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log("File Sent");
        } else {
            alert('An error occurred!');
        }
    };

    xhr.send(formData);

    return false;
}

function displayReturnedSolutions(solutions) {
    messageContainer = $(".messages ul");

    // If there is no solutions in the database show this message.
    if (solutions.length === 0) {
        sendAssistantMessage("Sorry, we couldn't find any solutions based on your input.")

    } else {

        for (var i = 0; i < solutions.length; i++) {
            messageContainer.append("<li class=\"text-center\"> <center class='results'><div class='chatProducts'><h5>"
                + solutions[i]["MajorTitle"] + "</h5><label>" + solutions[i]["SecondaryTitle"] + "</label><br><p>"
                + solutions[i]["ShortDescription"] + "</p><br><label>" + solutions[i]["Money"] +
                "</label><br><button onclick=\"openSolution('" + solutions[i]["URL"] +
                "')\" class='btn btn-primary chatProducts_button' style='vertical-align:middle'><span>View </span></button></div></center></li>");
        }
    }
    // submit answer automatically
    submitAnswer('');
}

function openSolution(link) {
    window.open(link);
}


// Blocks Renderer //
// --------------- //

function renderBlock(block) {
    currentBlock = block;
    if (currentBlock === undefined) {
        return 0;
    }

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
    $('#message-input').show();
    // to show the message from bot_user
    newMessage(BOT_USER, block.content.text);
    // to show answers related to question_block
    showAnswers(block.content.answers);

    function showAnswers(answers) {
        $messageInput = $("#message-input").first();
        $answersDiv = $("<div class='row text-center' style='padding:0 10px 10px'></div>");

        for (var i = 0; i < answers.length; i++) {
            $answersDiv.append("<button class=\"btn btn-primary answer\" onclick=\"submitAnswer(this.innerText, '" + answers[i].keywords + "' )\" >" + answers[i].text + "</button>");
            // $answersDiv.append("<div class='col-xs-2'><button class=\"btn btn-primary answer\" onclick=\"submitAnswer(this.innerText, '" + answers[i].keywords + "' )\" >" + answers[i].text + "</button></div>");
        }
        $messageInput.html($answersDiv);

        //$('.messages').css('height', 'calc(100% - 55px)');
        //$('.message-input').css('height', '55px');
    }
}

console.log(1)

function newMessage(from, text, html = false, isGif = false) {
    if (from == BOT_USER) {
        if (html)
            $('<li class="replies"><img src="/static/img/core-img/favicon-96x96.png" alt="" />' + text + '</li>').appendTo($('.messages ul')).hide().animate({
                opacity: 1,
                marginTop: '0px'
            }, 400);
        else
            $('<li class="replies"><img src="/static/img/core-img/favicon-96x96.png" alt="" /><p>' + text + '</p></li>').appendTo($('.messages ul')).animate({
                opacity: 1,
                marginTop: '0px'
            }, 400);
    }
    else {
        $('<li class="sent"><img src="https://cdn1.iconfinder.com/data/icons/social-messaging-productivity-1-1/128/gender-male2-512.png" alt="" /><p>' + text + '</p></li>').appendTo($('.messages ul'))
            .animate({
                opacity: 1,
                marginTop: '0px'
            }, 400);
    }
}

function renderUserInput(block) {
    // {#chatInputDiv.style = "display:block;";#}
    // {#fileUploadForm.style.display = 'none';#}

    $messageInput = $(".message-input").last();
    $userInput = $("<div class=\"wrap\" style=\"margin-top: 15px;min-height: 40px; background-color: white;\">\n" +
        "                <input onkeypress=\"handleEnter(event)\" " +
        "            id='textMessage' type=\"text\" placeholder=\"Write your message...\"/>\n" +
        "                <button onclick=\"submitAnswer('')\" class=\"submit\"><i class=\"fa fa-paper-plane\" aria-hidden=\"true\"></i></button>\n" +
        "            </div>");

    $('.messages').css('height', 'calc(100% - 40px)');

    $messageInput.append($userInput);
    sendAssistantMessage(block.content.text)
}

function renderFileUpload(block) {
    //$messageInput = $(".message-input").first();
    //$fileUpload = $("<div class=\"wrap\">\n" +
    //    "<input onkeypress=\"handleEnter(event)\" id=\"fileUploadB\" type=\"file\" placeholder=\"Write your message...\" style=\"\n" +
    //    "    background-color:  white;\n" + "\">" +
    //    "                <button onclick=\"submitAnswer('')\" class=\"submit\"><i class=\"fa fa-paper-plane\" aria-hidden=\"true\"></i></button>\n" +
    //    "            </div>");

    //$messageInput.html($fileUpload);

    //$('.messages').css('height','calc(100% - 40px)');
    //$('.message-input').css('height','40px');

    sendAssistantMessage(block.content.text);
    chatInputDiv.style = "display:block";
    fileUploadForm.style.display = 'block';
}

function renderSolutions(block) {
    $('.messages').css('height', '100%');
    $('.message-input').hide();
    $('#presetAnswers').hide();
    chatInputDiv.style = "display:none;";

    getSolutions(block.content.showTop)
        .then((solutions) => {
            solutions = JSON.parse(solutions);
            displayReturnedSolutions(solutions.data.solutions)
        })


}

async function submitAnswer(message) {
    // chatInputDiv.style = "display:none";#}
    // fileUploadForm.style.display = 'none';#}

    if (currentBlock.type == "Solutions") {
        await sleep(200);
        putThinkingGif();
        await sleep(thinkingGifLife);
        removeThinkingGif();
        await sleep(200);

        if (currentBlock.content.afterMessage) {
            sendAssistantMessage(currentBlock.content.afterMessage);

            await sleep(200);
            putThinkingGif();

            await sleep(thinkingGifLife);
            removeThinkingGif();
        }
        return getNextBlock(currentBlock.content.action, currentBlock.content.blockToGoID);
    }


    if (currentBlock.type == "File Upload") {
        //needs rework
        message = "&FILE_UPLOAD&" + document.getElementById("fileUploadB").value.split("\\")[document.getElementById("fileUploadB").value.split("\\").length - 1];
        if (!checkFileFormat(message)) {
            sendUserMessage(message.replace("&FILE_UPLOAD&", ""));

            await sleep(200);
            putThinkingGif();
            await sleep(thinkingGifLife);
            removeThinkingGif();
            await sleep(200);

            sendAssistantMessage("That did not match the allowed file types I've been given. They are " + getAllowedFormatsString() + ".")
            chatInputDiv.style = "display:block";
            fileUploadForm.style.display = 'block';
            return 0;
        }
        // clear file-upload div
        //$(".message-input").last().html('');
        //fileUploads.push(currentFileURL + ":::" + questionID + ":::" + message);

        newMessage(CLIENT_USER, message.replace("&FILE_UPLOAD&", ""));

        await sleep(200);
        putThinkingGif();
        await sleep(thinkingGifLife);
        removeThinkingGif();
        await sleep(200);

        print();

        if (currentBlock.content.afterMessage) {
            sendAssistantMessage(currentBlock.content.afterMessage);

            await sleep(200);
            putThinkingGif();
            await sleep(thinkingGifLife);
            removeThinkingGif();
            await sleep(200);
        }
        return getNextBlock(currentBlock.content.action, currentBlock.content.blockToGoID);
    }

    if (currentBlock.type == "User Input") { //validate user input
        if (message == "")
            message = document.getElementById("textMessage").value;

        if (message == "" || message.replace(/ /g, "") == "")
            return 0;

        $('#textMessage').val("");

        newMessage(CLIENT_USER, message.replace("&FILE_UPLOAD&", ""));

        print();

        await sleep(200);
        putThinkingGif();
        await sleep(thinkingGifLife);
        removeThinkingGif();
        await sleep(200);

        if (!validateUserInput(message, currentBlock.content.validation)) {
            sendAssistantMessage("I am sorry but that was not in the format I think it should be...");
            chatInputDiv.style = "display:block";
            return 0;
        }
        else {
            // clear user input div
            //$(".message-input").last().html('');
            if (currentBlock.content.afterMessage) {
                sendAssistantMessage(currentBlock.content.afterMessage);

                await sleep(200);
                putThinkingGif();
                await sleep(thinkingGifLife);
                removeThinkingGif();
                await sleep(200);

            }
        }
        return getNextBlock(currentBlock.content.action, currentBlock.content.blockToGoID);
    }
    var blockKeywords = undefined
    if (currentBlock.type == "Question") {
        // clear answers div
        $("#message-input").first().html('');
        newMessage(CLIENT_USER, message.replace("&FILE_UPLOAD&", ""));
        print();

        await sleep(200);
        putThinkingGif();
        await sleep(thinkingGifLife);
        removeThinkingGif();
        await sleep(400);

        var blockAnswers = currentBlock.content.answers;

        for (var i = 0; i < blockAnswers.length; i++) {
            if (blockAnswers[i].text == message) {
                if (blockAnswers[i].afterMessage) {
                    sendAssistantMessage(blockAnswers[i].afterMessage);

                    await sleep(200);
                    putThinkingGif();
                    await sleep(thinkingGifLife);
                    removeThinkingGif();
                    await sleep(400);

                }

                blockKeywords = blockAnswers[i].keywords;
                var action = blockAnswers[i].action;
                var blockToGoId = blockAnswers[i].blockToGoID;
                return getNextBlock(action, blockToGoId);
            }
        }
    }

    function print() {
        // print the selected answer
        if (blockKeywords)
            blockKeywords = Boolean(blockKeywords.split) ? blockKeywords.split(',') : blockKeywords;

        if (currentBlock.storeInDB) {
            var information = {
                "blockID": currentBlock.id,
                "questionText": currentBlock.content.text,
                "input": message
            };
            if (currentBlock.type == "Question" && blockKeywords !== undefined) {
                information["keywords"] = blockKeywords
                collectedInformation.push(information);
                addKeywords(blockKeywords)
            } else {
                information["keywords"] = []
                collectedInformation.push(information);
            }
        }

    }


}

function getNextBlock(action, blockToGoId = undefined) {
    var targetBlock = undefined;

    // Get next block based on action of the current block
    if (action === "Go To Next Block") {
        targetBlock = blocks[currentBlock.order]; //order starts from 1 and array from 0 so it just needs the current .order

    } else if (action === "Go To Specific Block") {
        for (var i = 0; i < blocks.length; i++) {
            if (blocks[i].order === blockToGoId) {
                targetBlock = blocks[i];
            }
        }
    } else if (action === "End Chat") {
        sendData().then((isSuccess) => {
            if (isSuccess) {
                sendAssistantMessage(currentBlock.afterMessage);
            } else {
                sendAssistantMessage("We apologise, your input couldn't be processed. Please contact us.");
            }
        });

        // End chat
        // SetRepeat();
        return 0;
    }

    // If not end chat and there is no next block
    if (targetBlock === undefined) {
        sendData().then((isSuccess) => {
            if (isSuccess) {
                // sendAssistantMessage("Thank you for your input. We'll be in touch.");#}
            } else {
                sendAssistantMessage("We apologise, your input couldn't be processed. Please contact us.");
            }

            SetRepeat();
            return 0;
        })
    }

    // If there is next block but not same as the current block
    if (currentBlock != undefined) { //check if its not trying to reload the same block
        if (currentBlock != targetBlock) {
            renderBlock(targetBlock);
        }
    }
}


function SetRepeat() {
    $("#optionsDiv").append("");
    newMessage(BOT_USER, "<div class='endChat' onclick=\"Reset()\"><a class='' style='width:400px;'>Search Again <i class=\"fa fa-refresh\" aria-hidden=\"true\"></i> </a></div>", true);
    //checkOutsideElements();
}

function Reset() {
    window.location.reload()
}


// helper functions
function sendUserMessage(message) {

    newMessage(CLIENT_USER, toEmoticon(message));
    // $("#messagesContainer").append("<div class='ucDiv'><li id='newMessage' class='userChat'>" + toEmoticon(message) + "</li></div>");#}
    // animateMessage("#newMessage");#}
    // document.getElementById('newMessage').id = 'oldMessage';#}
}

function sendAssistantMessage(message) {
    newMessage(BOT_USER, toEmoticon(message));
    // $("#messagesContainer").append("<div class='tsbDiv'><li id='newMessage' class='TSBbot'>" + toEmoticon(message) + "</li></div>");#}
    // animateMessage("#newMessage");#}
    // document.getElementById('newMessage').id = 'oldMessage';#}
}

function putThinkingGif() {
    newMessage(BOT_USER, '<img id=\'thinkingGif\' style="width:27px" id="thinkingGifIMG" src="/static/images/typingDots.gif">', false, true);
    // $(".messages ul").append('<li id="thinkingGif" class="replies"><img src="/static/img/core-img/favicon-96x96.png" alt="" /><p><img style="width:27px" id=\"thinkingGifIMG\" src="/static/images/typingDots.gif"></p></li>');#}
    // animateMessage("#thinkingGif");#}
}

function removeThinkingGif() {
    $("#thinkingGif").parent().parent().animate({
        marginTop: '100px',
        opacity: 0
    }, 300, () => {
        $("#thinkingGif").parent().parent().remove()
    })
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

        if (addIn) {
            keywords.push(blockKeywords[c]);
        }
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
    if (id == "#thinkingGif") {
        marginAnimate = "-=25px";
    }
    else if (id == "#newMessage") {
        marginAnimate = "-=35px";
    }
    $(id).animate({
        marginTop: marginAnimate
    }, "slow");
    if (!cancelScroll) {
        // scrollTo("chatBottom");#}
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
    // {#$('html, body').stop();#}
    // {#id = "#" + id#}
    // {#$('html, body').animate({#}
    // {#    scrollTop: ($(id).offset().top)#}
    // {# }, 2000);#}
    $(".messages").animate({scrollTop: $('.messages').prop("scrollHeight")}, "fast");

    // $(".messages").animate({scrollTop: $(document).height()}, "fast");#}
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
Object.defineProperty(Array.prototype, "equals", {enumerable: false});
