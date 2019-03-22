// // 基于准备好的dom，获取画布
// var myChart = echarts.init(document.getElementById('left3'),'dark');
//
// // 指定图表的配置项和数据
// var   option = {
//         legend: {},
//         tooltip: {
//             trigger: 'axis',
//             showContent: false
//         },
//         dataset: {
//             source: [
//                 ['product', '2012-2', '2013-2', '2014', '2015', '2016', '2017'],
//                 ['体育',      41.1,     30.4, 65.1, 53.3, 83.8, 98.7],
//                 ['Milk Tea', 86.5, 92.1, 85.7, 83.1, 73.4, 55.1],
//                 ['Cheese Cocoa', 24.1, 67.2, 79.5, 86.4, 65.2, 82.5],
//                 ['Walnut Brownie', 55.2, 67.1, 69.2, 72.4, 53.9, 39.1]
//             ]
//         },
//         xAxis: {type: 'category'},
//         yAxis: {gridIndex: 0},
//         grid: {top: '15%'},
//         series: [
//             {type: 'line', smooth: true, seriesLayoutBy: 'row'},
//             {type: 'line', smooth: true, seriesLayoutBy: 'row'},
//             {type: 'line', smooth: true, seriesLayoutBy: 'row'},
//             {type: 'line', smooth: true, seriesLayoutBy: 'row'}
//         ]
//     };
// // 使用刚指定的配置项和数据显示图表。
// myChart.setOption(option);