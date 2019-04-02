function f() {
    $.ajax({
        url: '/groupdata',
        type: 'GET',
        // data:
        dataType: 'json',
        success: function (data) {
            var myChart = echarts.init(document.getElementById('group1'), 'dark');
            // 记录标题的种类
            var legendsLength = data.kind.length
            // 记录班级的信息
            var classCount = data.className.length

            var xAxisData = [];
            var customData = [];
            var legendData = [];
            var dataList = [];
            legendData.push('trend');
            var encodeY = [];
            // 最终形成legend标题数组
            for (var i = 0; i < legendsLength; i++) {
                legendData.push(data.kind[i])
                dataList.push([])
                encodeY.push(1 + i);
            }
            for (var i = 0; i < classCount; i++) {  // 针对每个班级
                console.log(data.className)
                xAxisData.push(data.className[i]);
                var customVal = [i];
                customData.push(customVal);

                var data1 = dataList[0]
                var ave = []
                for (var j = 0; j < dataList.length; j++) { // 针对每个科目
                    dataList[j].push(average(data.data[i][j]))
                    customVal.push(average(data.data[i][j]));
                }
                console.log(ave)
            }

            console.log(dataList)
            console.log(data)

            // 指定图表的配置项和数据
            var option = {
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: legendData,
                    top: '5%',
                },
                grid: {top: '15%'},
                dataZoom: [{
                    type: 'slider',
                    start: 50,
                    end: 70
                }, {
                    type: 'inside',
                    start: 50,
                    end: 70
                }],
                xAxis: {
                    data: xAxisData
                },
                yAxis: {
                    type: 'value',
                    min: 0,
                    max: 17
                },
                series: [{
                    type: 'custom',
                    name: 'trend',
                    renderItem: renderItem,
                    itemStyle: {
                        normal: {
                            borderWidth: 2
                        }
                    },
                    encode: {
                        x: 0,
                        y: encodeY
                    },
                    data: customData,
                    z: 100
                }].concat(echarts.util.map(dataList, function (data, index) {
                    return {
                        type: 'bar',
                        animation: false,
                        name: legendData[index + 1],
                        itemStyle: {
                            normal: {
                                opacity: 0.5
                            }
                        },
                        data: data
                    };
                }))
            };
            myChart.setOption(option);
        }
    })
}

// 求每个科目的该班的平均分
function average(list) {
    let len = list.length
    let sum = 0;
    $.each(list, function (i, v) {
        sum += v;
    })
    console.log(sum);
    return sum / len;
}

// 进行折线渲染
function renderItem(params, api) {
    var xValue = api.value(0);
    var currentSeriesIndices = api.currentSeriesIndices();
    var barLayout = api.barLayout({
        barGap: '30%', barCategoryGap: '20%', count: currentSeriesIndices.length - 1
    });

    var points = [];
    for (var i = 0; i < currentSeriesIndices.length; i++) {
        var seriesIndex = currentSeriesIndices[i];
        if (seriesIndex !== params.seriesIndex) {
            var point = api.coord([xValue, api.value(seriesIndex)]);
            point[0] += barLayout[i - 1].offsetCenter;
            point[1] -= 20;
            points.push(point);
        }
    }
    var style = api.style({
        stroke: api.visual('color'),
        fill: null
    });

    return {
        type: 'polyline',
        shape: {
            points: points
        },
        style: style
    };
}


f()