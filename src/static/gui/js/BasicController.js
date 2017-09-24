angularApp.controller("BasicController", function BasicController($scope, $http, $rootScope) {
    $rootScope.ptirs = [];
    $scope.ptirData = {}
    $scope.ip_addr = "localhost"

    $('.modala').hide();
    $('.lst').show();

    $http({
        method: "GET",
        url: "http://" + $scope.ip_addr + ":7421/getPtirs"
    }).then(function success(response) {
        $rootScope.ptirs = [];
        for (var i = 0; i < response.data.length; i++) {
            var item = {};
            item["ptirId"] = response.data[i]["_id"];
            item["reporter"] = response.data[i]["reporter"];
            item["assignee"] = response.data[i]["assignee"];
            item["severity"] = response.data[i]["severity"];
            item["status"] = response.data[i]["status"];
            item["description"] = response.data[i]["description"];

            $rootScope.ptirs.push(item);
        }
    }, function failure(response) {
        alert("Error getting response from /getptirs " + response.toString() + " " + response);
    });

    $scope.showModel = function () {
        alert('called');
        $('.modala').show();
        $('.lst').hide();
    }

    $scope.save = function() {
        alert('save');
        $scope.ptirData['reporter'] = $scope.ptir.reporter
        $scope.ptirData['assignee'] = $scope.ptir.assignee
        $scope.ptirData['severity'] = $scope.ptir.severity
        $scope.ptirData['status'] = $scope.ptir.status
        $scope.ptirData['description'] = $scope.ptir.description
        $http({ 
                method: "POST",
                url: "http://" + $scope.ip_addr + ":7421/addPtir",
                data: JSON.stringify($scope.ptirData)
        }).then(function success(response) {
            alert("success " + response.toString());
            $rootScope.push($scope.ptirData)
        }, function failure(response) {
            alert('error in post ptir');
        });
        $('.modala').hide();
        $('.lst').show();
    }
});

