angularApp.controller("BasicController", function BasicController($scope, $http, $rootScope) {
    $rootScope.ptirs = [];

    $http({
        method: "GET",
        url: "http://192.168.0.106:7421/getPtirs"
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
        $('.ui.modal')
            .modal('show');
    }
});

