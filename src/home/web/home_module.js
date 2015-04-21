(function () {
    angular.module('finance.projectHours',
        [
            'ui.bootstrap',
            'ngRoute',
            'ngCookies',
            'gettext',
            'chart.js',
            'smart-table',
            'ngSanitize',
            'ngCsv'
        ]
    );

    angular.module('finance.projectHours')
        .run(function ($location, $cookies, $rootScope) {
            //console.log('cookie = '+ $cookieStore.get('ate_user'));
            $rootScope.$on('$routeChangeStart', function (scope, next, current) {
                //in case of refresh - the current page is undefined
                if (typeof(current) == "undefined" || $location.path == '/login') {
                    $location.path($location.path())
                }
                else {
                    if (!$cookies.project_hours) {
                        $location.path("/login")
                    }
                }
            });
        })

}());

