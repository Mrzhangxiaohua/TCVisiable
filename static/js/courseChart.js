function courseCharts() {
    var myChart = echarts.init(document.getElementById('container1'));

    // 指定图表的配置项和数据
    var option = {
    series : [
        {
            name: '访问来源',
            type: 'pie',
            radius: '55%',
            center : ['50%', '50%'],
            roseType: 'angle',
            data:[
                {value:235, name:'视频广告'},
                {value:274, name:'联盟广告'},
                {value:310, name:'邮件营销'},
                {value:335, name:'直接访问'},
                {value:400, name:'搜索引擎'}
            ]
        }
    ]
};

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
courseCharts();