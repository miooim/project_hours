(function () {

    function routes($routeProvider) {
        $routeProvider
            .when('/admin', {
                templateUrl: '/static/src/admin/web/ph_admin.html',
                controller: 'ProjectHoursAdminController',
                controllerAs: 'ad'
            })
    }

    angular.module('finance.projectHours')
        .config(['$routeProvider', routes]);
}());

