function grade(data) {
    alert(data)
    var data = data;
    $.ajax({
        url: '/getStuId',
        type: 'GET',
        data: {"data": data},
        dataType: 'json',
        success: function (data) {
            var myChart = echarts.init(document.getElementById('left3'),'dark');
            var source = dataProcess(data);
            console.log(source)
            var serie = []
            for (var i = 0; i < data["examType"].length; i++) {
                serie.push({type: 'line', smooth: true, seriesLayoutBy: 'row'})
            }
            var option = {
                legend: {},
                tooltip: {
                    trigger: 'axis',
                    showContent: true
                },
                dataset: {
                    source: source
                },
                xAxis: {type: 'category'},
                yAxis: {gridIndex: 0},
                grid: {top: '15%'},
                series: serie
            };
            myChart.setOption(option);
        }
    });
}

// 数据处理函数
function dataProcess(data) {
    console.log(data);
    var source = [];
    var dataAll = data["data"];
    var examTime = data["examTime"]; // 2018-2019-1
    var examType = data["examType"]; // 语文数学英语
    var xAxis = []
    xAxis.push("product")
    $.each(examTime,function (i,v) {
        xAxis.push(v["exam_numname"])
    })
    source.push(xAxis)
    // source.push(examTime)   // 得到x轴的坐标表示
    for (var i = 0; i < examType.length; i++) { // 拿到abc
        var temp = []
        temp.push(examType[i]["mes_sub_name"])
        for (var j = 0; j < examTime.length - 1; j++) { //拿到2016，2017
            var daa = checkHasGrade(examType[i]["mes_sub_name"], examTime[j]["exam_numname"], dataAll);
            temp.push(daa);
        }
        source.push(temp);
    }
    return source;
}

// 成绩整理成Echarts图标格式
function checkHasGrade(mes_sub_name, exam_numname, dataAll) {
    for (var i = 0; i < dataAll.length; i++) {
        if (dataAll[i]["exam_numname"] == exam_numname && dataAll[i]["mes_sub_name"] == mes_sub_name) {
            return dataAll[i]["mes_Score"];
        }
    }
    return 0;
}