(function () {
    /**
     * Login Controller using the following services:
     * @param $scope
     * @param $cookieStore
     * @param $http
     * @param $location
     * @constructor
     * @param $cookies
     * @param $timeout
     */
    function LoginController($scope, $cookieStore, $http, $location, $cookies, $timeout) {
        var self = this;
        self.username = '';
        self.password = '';
        self.error = '';
        self.debug = '';
        self.next = '';

        self.afterLogin = function () {
            $location.path('/');
        };
        /**
         * Login with username password & load user's permissions
         *
         * User permissions are stored in AuthService so they are accessible to all other contollers
         */
        self.login = function () {
            var data = {username: self.username, password: self.password};
            $http.post('/api/accounts', data).success(function (data, status, headers, config) {
                console.log(data);
                if (data.status == 0) {
                    console.log('login success');


                     //use timeout to make sure cookie is set
                     $timeout(function(){
                     $location.path('/home');
                     },300);

                } else {
                    self.error = data.error;
                    //self.error = 'Server Error - please contact a technician';
                    self.debug = data.debug;
                    self.username = '';
                    self.password = '';
                    console.log('login fail');
                    console.log(data);
                }
            }).error(function (data, status, headers, config) {
                self.error = 'Server Error - please contact a technician';
                self.debug = data;
            });
        };
        self.logout = function () {
            console.log('logout');
            var data = {};
            $http.put('/api/accounts', data).success(function (data, status, headers, config) {
                // this callback will be called asynchronously
                console.log(data);
                if (data.status == 0) {
                    //delete $rootScope.userProfile;
                    //console.log($cookieStore.get('ate_user_prof'));
                    $cookieStore.remove('project_hours');
                    $location.path('/login');
                    //console.log(document.cookie);
                } else {
                    console.log(data)
                }

            }).error(function (data, status, headers, config) {
                console.log(data)
            });
        };
    }

    angular.module('finance.projectHours')
        .controller('LoginController', ['$scope', '$cookieStore', '$http', '$location', '$cookies', '$timeout',
            LoginController]);
}());