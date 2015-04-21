(function () {

    function routes($routeProvider) {
        $routeProvider
            .when('/home', {
                templateUrl: '/static/src/home/web/home/home_view.html',
                controller: 'HomeController',
                controllerAs: 'home'
            })
            .when('/login', {
                templateUrl: '/static/src/auth/web/login.html',
                controller: 'LoginController',
                controllerAs: 'login'
            })
        .otherwise({redirectTo: '/home'});
    }

    angular.module('finance.projectHours')
        .config(['$routeProvider', routes]);
}());

