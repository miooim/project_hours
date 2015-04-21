(function () {

    function routes($routeProvider) {
        $routeProvider
            .when('/projectHours', {
                templateUrl: '/static/src/project_hours/web/ph.html',
                controller: 'ProjectHoursController',
                controllerAs: 'ph'
            })
            .when('/projectHours/:month/:year', {
                templateUrl: '/static/src/project_hours/web/ph.html',
                controller: 'ProjectHoursController',
                controllerAs: 'ph'
            })
    }

    angular.module('finance.projectHours')
        .config(['$routeProvider', routes]);
}());

