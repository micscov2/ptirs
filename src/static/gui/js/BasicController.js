angularApp.controller("BasicController", function BasicController($scope, $http, $rootScope) {
    $rootScope.ptirs = [];
    $rootScope.totalPtirs = [];
    $scope.ptirData = {}
    $scope.userData = {}
    $scope.ip_addr = "172.16.147.129"
    $scope.currPageNum = 0;
    const pageSize = 5;
    offSet = 0;
    totalPages = -1;

    $('.modala').hide();
    $('.lst').show();

    $scope.saveUser = function() {
        $scope.userData['name'] = $scope.user.name
        $scope.userData['password'] = $scope.user.password
        $scope.userData['email'] = $scope.user.email
        $scope.userData['role'] = $scope.user.role

        $http({
            method: "POST",
            url: "http://" + $scope.ip_addr + ":7421/addUser",
            data: JSON.stringify($scope.userData)
        }).then(function success(response) {
            alert("Success!")
        }, function failure(response) {
            alert("Error getting response from /getUsers " + response.toString())
        });
    };

    $scope.pageChange = function(num) {
        console.log(num);
        if (num == "0") {
            if ($scope.currPageNum != 0) {
                $scope.currPageNum -= 1;
                $scope.reload('1');
            }
        } else if (num == "1") {
            if ($scope.currPageNum < totalPages) {
                $scope.currPageNum += 1;
                $scope.reload('1');
            }
        }
    }

    $scope.reload = function(code) {
        // debug;
        filter = "";
        if ($scope.open && !$scope.inProgress) {
            filter = 'OPEN'
        } else if ($scope.inProgress && !$scope.open) {
            filter = 'IN PROGRESS'
        } else if ($scope.inProgress && $scope.open) {
            filter = 'OPEN,IN PROGRESS'
        }

        if (!filter) {
            filter = 'all';
        }

        keyz = "output"
        if ($scope.keyphrase) {
            keyz = $scope.keyphrase;
        }

        if (code == '0') {
            $http({
                method: "GET",
                url: "http://" + $scope.ip_addr + ":7421/getPtirs/" + filter + "/" + keyz
            }).then(function success(response) {
                $rootScope.ptirs = [];
                $rootScope.totalPtirs = [];
                totalPages = response.data.length / pageSize;

                for (var i = 0; i < response.data.length; i++) {
                    var item = {};
                    item["ptirId"] = response.data[i]["_id"];
                    item["reporter"] = response.data[i]["reporter"];
                    item["assignee"] = response.data[i]["assignee"];
                    item["severity"] = response.data[i]["severity"];
                    item["status"] = response.data[i]["status"];
                    item["description"] = response.data[i]["description"];
                    item["created_on"] = response.data[i]["created_on"];

                    $rootScope.totalPtirs.push(item);

                    if (i < pageSize) {
                        $rootScope.ptirs.push(item);
                    }

                    $scope.currPageNum = 0;
                }
            }, function failure(response) {
                alert("Error getting response from /getptirs " + response.toString() + " " + response);
            });
        } else {
            $rootScope.ptirs = [];
            for (var i = $scope.currPageNum * pageSize; i < ($scope.currPageNum + 1) * pageSize; i++) {
                var item = {};

                item["ptirId"] = $rootScope.totalPtirs[i]["ptirId"];
                item["reporter"] = $rootScope.totalPtirs[i]["reporter"];
                item["assignee"] = $rootScope.totalPtirs[i]["assignee"];
                item["severity"] = $rootScope.totalPtirs[i]["severity"];
                item["status"] = $rootScope.totalPtirs[i]["status"];
                item["description"] = $rootScope.totalPtirs[i]["description"];
                item["created_on"] = $rootScope.totalPtirs[i]["created_on"];

                $rootScope.ptirs.push(item);
            }
        }


    };

    $scope.showModel = function() {
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
        $scope.ptirData['created_on'] = $scope.ptir.created_on

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
            for (var i = 0; i < $scope.totalPtirs.length; i++) {
                if (currPtirId == $scope.totalPtirs[i].ptirId.toString()) {

                    $scope.ptir.reporter = $scope.totalPtirs[i].reporter;
                    $scope.ptir.assignee = $scope.totalPtirs[i].assignee;
                    $scope.ptir.severity = $scope.totalPtirs[i].severity;
                    $scope.ptir.status = $scope.totalPtirs[i].status;
                    $scope.ptir.description = $scope.totalPtirs[i].description;
                    $scope.ptir.created_on = $scope.totalPtirs[i].created_on;
                    break;
                }
            }
            return;
        }

        $scope.ptirData['reporter'] = $scope.ptir.reporter
        $scope.ptirData['assignee'] = $scope.ptir.assignee
        $scope.ptirData['severity'] = $scope.ptir.severity
        $scope.ptirData['status'] = $scope.ptir.status
        $scope.ptirData['description'] = $scope.ptir.description
        $scope.ptirData['created_on'] = $scope.ptir.created_on
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
