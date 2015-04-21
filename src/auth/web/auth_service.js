(function () {
    /**
     * AuthService handles user permissions
     *
     * @param $http
     * @returns {AuthService}
     * @constructor
     * @param $cookies
     * @param $location
     */
    function AuthService($http, $location) {

        /**
         * logout a user and
         * @param next - a url to navigate after the logout
         */
        self.logout = function () {
            console.log('logout');
            var data = {};
            $http.put('/api/accounts', data).success(function (data, status, headers, config) {
                console.log(data);
                if (data.status == 0) {
                    $location.path('/login');
                } else {
                    console.log(data)
                }

            }).error(function (data, status, headers, config) {
                console.log(data)
            });
        };

        return self;
    }

    angular.module('finance.projectHours')
        .service('AuthService', ['$http', '$location', AuthService])
}());