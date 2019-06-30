var pieData = [
            {% for item,label,colors in set %}
                {
                    value: {{item}},
                    label: "{{label}}",
                    color : "{{colors}}"
                },
                {% endfor %}


         ];

   // get bar chart canvas
   var mychart = document.getElementById("chart").getContext("2d");

   steps = 10;
   max = 10;
   // draw pie chart
   new Chart(document.getElementById("chart").getContext("2d")).Pie(pieData);
