
const assistantID = window.location.pathname.split('/')[3];
let popularSolutions = undefined;
let totalReturnedSolutions = undefined;
let timeSpentAvgOvertime = undefined;
let usersOvertime = undefined;
let totalQuestionsOverMonth = undefined;
let totalSolutionsOverMonth = undefined;
let usersTotal = undefined;

function getAnalytics(){
    $.ajax({
        contentType: 'application/json',
        dataType : 'json',
        url: ' /admin/assistant/' + assistantID +'/analytics/data',
        type: "GET"
    }).done(function (res) {

        console.log("Analytics retrieved successfully!");

        popularSolutions = res.data.popularSolutions;
        totalReturnedSolutions = res.data.totalReturnedSolutions;
        timeSpentAvgOvertime = res.data.timeSpentAvgOvertime;
        totalQuestionsOverMonth = res.data.TotalQuestionsOverMonth.reverse();
        totalSolutionsOverMonth = res.data.TotalSolutionsOverMonth.reverse();
        console.log("res.data.usersOvertime: ", res.data.UsersOvertime);
        usersOvertime = res.data.UsersOvertime.reverse();
        usersTotal = res.data.TotalUsers;
        //console.log(usersOvertime.reverse());
        // renderChartJS("line", "line-chart", ["2017-07-04T01:51:02-06:00", "2017-07-04T10:51:02-06:00"], usersOvertime.reverse(), "Total Number of Players Playing", "Date", "Players", "188,4,0", 0); // Number of players
        loadGraphs()

    }).fail(function (res) {
        console.log("Error in retrieving analytics data.");
        console.log(res);
    });
}

function loadGraphs(){
    console.log("usersOvertime: ", usersOvertime);
    var weeklyLabels = getWeeklyLabels(usersOvertime)
    var chartData = {
        labels: weeklyLabels,
        datasets: [{
            label: 'Users Overtime',
            fill: true,
            lineTension: 0.2,
            backgroundColor: "rgb(193,140,227, 0.5)",
            borderColor: "rgb(138,43,226)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgb(75,0,130)",
            //pointBackgroundColor: "#fff",
            pointBorderWidth: 0,
            pointHoverRadius: 2,
            //pointHoverBackgroundColor: "rgba(75,192,192,1)",
            //pointHoverBorderColor: "rgba(220,220,220,1)",
            //pointHoverBorderWidth: 2,
            pointRadius: 0,
            pointHitRadius: 10,
            data: usersOvertime,
            spanGaps: true
        }]
    };



    new Chart(document.getElementById("line-chart1").getContext("2d"), {
        type: 'line',
        data: chartData,
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        fontSize: 7
                    }
                }]
            }
        }
    });

    //TOTAL USERS
    $("#totalUsersh1").html(usersTotal);

    //TOTAL QUESTIONS ANSWERED OVER TIME

    var chartData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [{
            label: 'Total Questions Answered',
            fill: false,
            lineTension: 0.3,
            backgroundColor: ["rgb(186,85,211)", "rgb(148,0,211)", "rgb(153,50,204)", "rgb(139,0,139)", "rgb(128, 0, 128)", "rgb(75,0,130)", "rgb(147,112,219)", "rgb(128,0,128)", "rgb(147,112,219)"],
            borderColor: "rgb(138,43,226)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 0.5,
            pointHitRadius: 10,
            data: totalQuestionsOverMonth,
            spanGaps: false
        }]
    };
    new Chart(document.getElementById("bar-chart1").getContext("2d"), {
        type: 'bar',
        data: chartData,
        options: { 
            scales: {
                xAxes: [{
                    gridLines: {
                        color: "rgba(0, 0, 0, 0)",
                    }
                }]
            }
        } 
    });

    //TOTAL SOLUTIONS RETURNED OVER TIME

    var chartData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [{
            label: 'Total Solutions Returned',
            fill: false,
            lineTension: 0.3,
            backgroundColor: ["rgb(186,85,211)", "rgb(148,0,211)", "rgb(153,50,204)", "rgb(139,0,139)", "rgb(128, 0, 128)", "rgb(75,0,130)", "rgb(147,112,219)", "rgb(128,0,128)", "rgb(147,112,219)"],
            borderColor: "rgb(138,43,226)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 0.5,
            pointHitRadius: 10,
            data: totalSolutionsOverMonth,
            spanGaps: false
        }]
    };
    new Chart(document.getElementById("bar-chart2").getContext("2d"), {
        type: 'bar',
        data: chartData,
        options: {
            scales: {
                xAxes: [{
                    gridLines: {
                        color: "rgba(0, 0, 0, 0)",
                    }
                }]
            }
        } 
    });
}

function getWeeklyLabels(records) {
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var returnArray = [];
    var lastMonth = 0;
    var currentMonth = 0;
    for (var i = 0; i < records.length; i++) {
        currentMonth = parseInt(records[i].x.split("-")[1]);
        if (currentMonth != lastMonth) {
            returnArray.push(months[currentMonth - 1]);
            lastMonth = currentMonth;
        } else {
            returnArray.push("");
        }
    }

    return returnArray
}

function g(length){
    let l = [];
    for(var i=0; i<length; i++){
        l.push("")
    }
    return l;
}

function renderChartJS(chartType, elemId, labels, data, title, xAxisLabel, yAxisLabel, rgbaColorStr, yMax) {
   var feb = g(29);
   var bigM = g(31);
   var normalM = g(30);

   var months = ['January', 'February', 'March', 'April', 'May', 'June','July','August','September','October','November','December'];
    var days = [31,29,31,30,31,30,31,30,31,30,31,30];
    var headings = [];
    for(var i=0;i<months.length;i++){
       headings.push(months[i]);
       for(var c=0;c<days.length - 1;c++){
           headings.push("");
       }
    }
   if (data.length) {
      var ctx = document.getElementById(elemId).getContext('2d');
      var myChart = new Chart(ctx, {
         type: chartType,
         data: {
            labels: headings,
            datasets: [{
               data: data,
               borderColor: "rgba(" + rgbaColorStr + ",1)",
               backgroundColor: "rgba(" + rgbaColorStr + ",0.5)"
            }]
         },
         options: {
            title: {
               display: true,
               text: title
            },
             showXLabels: 5,
          //   scales: {
          //  xAxes: [{
          //     type: 'time',
          //     position: 'bottom',
          //     time: {
          //       displayFormats: {'day': 'MM/YY'},
          //       tooltipFormat: 'DD/MM/YY',
          //       unit: 'year'
          //      }
          //   }],
          //   yAxes: [{
          //       ticks: {
          //           max:10,
          //           min: 0,
          //           stepSize: 1
          //       }
          //   }]
          // }

         }
      });
   }
}


getAnalytics();