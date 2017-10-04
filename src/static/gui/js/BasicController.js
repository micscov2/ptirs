angularApp.controller("BasicController", function BasicController($scope, $http, $rootScope) {
    $rootScope.ptirs = [];
    $scope.ptirData = {}
    $scope.ip_addr = "localhost"

    $('.modala').hide();
    $('.lst').show();


    $scope.reload = function() {
        // debug;
        filter = "";
        if ($scope.open) {
            filter = 'OPEN'
        } else if ($scope.inProgress) {
            filter = 'IN PROGRESS'
        }

        if (! filter) {
            filter = 'all';
        }

        keyz = "output"
        if ($scope.keyphrase) {
            keyz = $scope.keyphrase;
        }

        $http({
            method: "GET",
            url: "http://" + $scope.ip_addr + ":7421/getPtirs/" + filter + "/" + keyz
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


    };

    // $http({
    //     method: "GET",
    //     url: "http://" + $scope.ip_addr + ":7421/getPtirs/all"
    // }).then(function success(response) {
    //     $rootScope.ptirs = [];
    //     for (var i = 0; i < response.data.length; i++) {
    //         var item = {};
    //         item["ptirId"] = response.data[i]["_id"];
    //         item["reporter"] = response.data[i]["reporter"];
    //         item["assignee"] = response.data[i]["assignee"];
    //         item["severity"] = response.data[i]["severity"];
    //         item["status"] = response.data[i]["status"];
    //         item["description"] = response.data[i]["description"];

    //         $rootScope.ptirs.push(item);
    //     }
    // }, function failure(response) {
    //     alert("Error getting response from /getptirs " + response.toString() + " " + response);
    // });

    $scope.showModel = function () {
        // alert('called');
        $('.modala').show();
        $('.lst').hide();
    }

    $scope.update = function() {
        $scope.ptirData['_id'] = $scope.currPtirId
        $scope.ptirData['reporter'] = $scope.ptir.reporter
        $scope.ptirData['assignee'] = $scope.ptir.assignee
        $scope.ptirData['severity'] = $scope.ptir.severity
        $scope.ptirData['status'] = $scope.ptir.status
        $scope.ptirData['description'] = $scope.ptir.description

        $scope.currPtirId = 0

        $http({ 
                method: "POST",
                url: "http://" + $scope.ip_addr + ":7421/updatePtir",
                data: JSON.stringify($scope.ptirData)
        }).then(function success(response) {
            // alert("success " + response.toString());
            $rootScope.ptirs.push($scope.ptirData)
        }, function failure(response) {
            alert('error in post ptir');
        });
        $('.modala').hide();
        $('.lst').show();
    };

    $scope.save = function(change) {
        if (change) {
            currPtirId = $scope.currPtirId;
            // alert(currPtirId);
            for (var i = 0; i < $scope.ptirs.length; i++) {
                if (currPtirId == $scope.ptirs[i].ptirId) {

                    $scope.ptir.reporter = $scope.ptirs[i].reporter;
                    $scope.ptir.assignee = $scope.ptirs[i].assignee;
                    $scope.ptir.severity = $scope.ptirs[i].severity;
                    $scope.ptir.status = $scope.ptirs[i].status;
                    $scope.ptir.description = $scope.ptirs[i].description;
                    break;
                }
            }
            return;
        } 
        // alert('save');
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
            // alert("success " + response.toString());
            $rootScope.ptirs.push($scope.ptirData)
        }, function failure(response) {
            alert('error in post ptir');
        });
        $('.modala').hide();
        $('.lst').show();
    }
});

