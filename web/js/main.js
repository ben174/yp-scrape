var ypScrapeApp = angular.module('ypScrapeApp', []);

ypScrapeApp.controller('YpScrapeCtrl', function ($scope, $http) {
    $scope.items = [];

    $scope.ypquery = {
        query: 'cupcakes',
        location: 'Tucson, AZ',
        project: 'yp',
        spider: 'ypcrawl'
    };

    $scope.jobid = null;

    $scope.runQuery = function () {
        // http://192.168.99.100:32768/schedule.json -d project=yp -d spider=ypcrawl -d query=tacos
        url = '/job';
        console.log(url);
        $http({
            method: 'POST',
            url: url,
            data: $scope.ypquery
        }).then(function successCallback(response) {
            console.log("job started");
            console.log(response);
            $scope.jobid = response.data.jobid;
            // begin polling job
            $scope.pollJob()

        }, function errorCallback(response) {
        });
    };

    $scope.pollJob = function () {
        $http({
            method: 'GET',
            url: '/job/' + $scope.jobid
        }).then(function successCallback(response) {
            console.log("Job state: " + response.data.state);
            if(response.data.state == 'running' || response.data.state == 'finished') {
                $scope.getResults();
            }
            if(response.data.state == 'pending' || response.data.state == 'running') {
                setTimeout($scope.pollJob, 1000);
            }
        }, function errorCallback(response) {
        });
    };

    $scope.getResults = function () {
        $http({
            method: 'GET',
            url: '/log/' + $scope.jobid
        }).then(function successCallback(response) {
            $scope.items = response.data;
        }, function errorCallback(response) {
        });
    };

    $scope.webSocket = function () {
        // unused - abandoned attempt to do this through websockets
        var ws = new WebSocket("ws://127.0.0.1:8888/scrape/cupcake/94536");
        ws.onmessage = function (data) {
            $scope.$apply(function () {
                console.log(data.data);
                $scope.items.push(data.data);
            });
        }
    };
});
