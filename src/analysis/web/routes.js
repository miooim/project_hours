(function () {

    function routes($routeProvider) {
        $routeProvider
            .when('/analysis', {
                templateUrl: '/static/src/analysis/web/analysis.html',
                controller: 'AnalysisController',
                controllerAs: 'an'
            })
    }

    angular.module('finance.projectHours')
        .config(['$routeProvider', routes]);
}());

