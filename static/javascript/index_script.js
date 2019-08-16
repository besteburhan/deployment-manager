$(document).ready(function() {
    $("#stat-select").change(function () {
        var select_div = document.getElementById("stat-select");
        var value = select_div.options[select_div.selectedIndex].value;
        if ( value == 1){
            $.ajax({
                type: 'get',
                url: '',
                data: {
                    'value': value,
                },
                success: function (data_from_index) {

                  var datapoints = data_from_index.datapoints;
                  var names_user = data_from_index.names_user;
                  var chart = new CanvasJS.Chart("chartContainer", {
                        animationEnabled: true,
                        title:{
                            text: ""
                        },
                        axisX: {
                            title:"The Number of Projects"
                        },
                        axisY:{
                            title: "The Number of Deployments"
                        },
                        data: [{
                            markersize: 20,
                            name: "Users' projects and deployments count",
                            type: "scatter",
                            toolTipContent: "<span style=\"color:#4F81BC \"></span><br/><b> Username:</b> {name} <br/><b> Project count:</b></span> {x} <br><b> Deployment Count:</b></span> {y} ",
                            showInLegend: true,
                            dataPoints: []
                        }],

                    });
                    var ind_for_name = 0;
                    for(var i = 0; i < datapoints.length; i++) {
                        var colors = ['#308bb9','#278521','#851915','#851f7d'];
                        for(var j=0; j <datapoints[i].length; j++) {
                            chart.options.data[0].dataPoints.push({
                                x: parseFloat(datapoints[i][j][0]),
                                y: parseFloat(datapoints[i][j][1]),
                                name: names_user[ind_for_name++],
                                color: colors[i],
                            });
                        }
                    }
                    chart.render();

                },
                error: function (data) {
                  alert("error ");
                },
              });
         }
        else if (value == 2){
            $.ajax({
                type: 'get',
                url: '',
                data: {
                    'value': value,
                },
                success: function (data_from_index) {

                  var datapoints = data_from_index.datapoints;
                  var names_user = data_from_index.names_user;
                  var chart2 = new CanvasJS.Chart("chartContainer", {
                        animationEnabled: true,
                        title:{
                            text: ""
                        },
                        axisX: {
                            title:"The Number of Teams"
                        },
                        axisY:{
                            title: "The Number of Projects"
                        },
                        data: [{
                            markersize: 10,
                            name: "Users' Teams and Projects count",
                            type: "scatter",
                            toolTipContent: "<span style=\"color:#4F81BC \"></span><br/><b> Username:</b> {name} <br/><b> Project count:</b></span> {x} <br><b> Deployment Count:</b></span> {y} ",
                            showInLegend: true,
                            dataPoints: []
                        }],

                    });
                    var ind_for_name = 0;
                    for(var i = 0; i < datapoints.length; i++) {
                        colors = ['#2a7aa2','#37ba2e','#ac201b','#bf2db4'];
                        for(var j=0; j <datapoints[i].length; j++) {
                            chart2.options.data[0].dataPoints.push({
                                x: parseFloat(datapoints[i][j][0]),
                                y: parseFloat(datapoints[i][j][1]),
                                name: names_user[ind_for_name++],
                                color: colors[i],
                            });
                        }
                    }
                    chart2.render();
                },
                error: function (data) {
                  alert("error ");
                },
              });
         }
    });

    var loading = $('#loadingDiv').hide();
    $(document)
        .ajaxStart(function () {
            loading.show();
        })
        .ajaxStop(function () {
            loading.hide();
        });
});