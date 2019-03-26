// 地图js,主界面的地图交互，取学生id
var options = {
    size: BMAP_POINT_SIZE_SMALL,
    shape: BMAP_POINT_SHAPE_STAR,
    color: '#D3D120'
}
$.ajax({
    url: "testdb",
    type: "post",
    dataType: "json",
    success: function (result) {
        console.log(result)
        var points = []
        var myGeo = new BMap.Geocoder();
        var stuLocation = {}

        function getLocation(j) {
            myGeo.getPoint(result[j].bf_NativePlace, function (point) {
                if (point) {
                    var random = Math.random() * 0.1
                    points.push(new BMap.Point(point.lng - random, point.lat - random));
                }
                return setTimeout(function () {
                    // console.log(result[j].bf_StudentID,point)
                    // console.log(random)
                    stuLocation[(Number(point.lng) - Number(random)) + ',' + (Number(point.lat) - random)] = {
                        "stuId": result[j].bf_StudentID
                    }
                }, 700)
            })
        }

        for (var j = 0; j < result.length; j++) {
            getLocation(j)
        }

        var pointCollection = new BMap.PointCollection(points, options);
        map.addOverlay(pointCollection);
        console.log(stuLocation)

        pointCollection.addEventListener('click', function (e) {
            // console.log(stuLocation[e.point.lng + ',' + e.point.lat])
            var stuId = stuLocation[e.point.lng + ',' + e.point.lat]['stuId'];
            grade(stuId);
            // alert('单击点的坐标为：' + e.point.lng + ',' + e.point.lat + "学生ID" + stuLocation[e.point.lng + ',' + e.point.lat]['stuId']);  // 监听点击事件
        });
    }
})
