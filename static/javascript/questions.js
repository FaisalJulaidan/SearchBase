// set variables
var oldNOQ = 0;
var maxQuestions = 10;

// set the question form template
var qTemplate1 = "<div class = \"Questions\"><label class=\"control-label col-md-3 col-sm-3 col-xs-12\" for=\"last-name\">"
var qTemplate2 = " question <span class=\"required\">*</span></label><div class=\"col-md-6 col-sm-6 col-xs-12\"><input type=\"text\" name=\""
var qTemplate3 = "\" required=\"required\" class=\"form-control col-md-7 col-xs-12\"></input></div><br /><br /></div>";

// set event listeners
document.getElementById("NOQ-ResetB").addEventListener("click", ClearNOQ);
document.getElementById("NOQ-SubmitB").addEventListener("click", ChangeNofQuestions);
document.getElementById("QTemplate-ResetB").addEventListener("click", ClearQTemplate);
document.getElementById("QTemplate-SubmitB").addEventListener("click", ClearQTemplate);

// TODO QTemplate-SubmitB

// called on NOQ Reset Click
function ClearNOQ(){
  document.getElementById("number-of-questions").value = "";
  $("#QuestionDiv").empty();
  oldNOQ = 0;
}

// called on NOQ Submit Click
function ChangeNofQuestions(){
  var noq = parseInt(document.getElementById("number-of-questions").value);
  if(!Number.isNaN(noq)){
    if(noq <= maxQuestions){
      if(noq > oldNOQ){
        for(i = oldNOQ; i < noq; i++){
          var number;
          if(i == 0){ number = "First" }
          if(i == 1){ number = "Second" }
          if(i == 2){ number = "Third" }
          if(i == 3){ number = "Fourth" }
          if(i == 4){ number = "Fifth" }
          if(i == 5){ number = "Sixth" }
          if(i == 6){ number = "Seventh" }
          if(i == 7){ number = "Eight" }
          if(i == 8){ number = "Ninth" }
          if(i == 9){ number = "Tenth" }
          console.log(i + " JEREE");
          $("#QuestionDiv").append(qTemplate1 + number + qTemplate2 + "question" + (i + 1) + qTemplate3);
          // add preset question to fill
        }
      } else if(noq < oldNOQ) {
        for(i = oldNOQ; i > noq; i--){
          $(".Questions")[$(".Questions").length - 1].remove();
        }
      }
      oldNOQ = noq;
    }
  }
}

function ClearQTemplate(){
  $("#QuestionDiv input").val("");
}
