(function () {
    /**
     * Login Controller using the following services:

     * @param $cookies
     * @param AuthService
     */
    function MenuController($cookies, AuthService) {
        var self = this;

        self.username = function () {
            if ($cookies.project_hours) {
                return $cookies.project_hours;
            } else {
                return '';
            }
        };

        self.logout = function () {
            return AuthService.logout();
        };
    }

    angular.module('finance.projectHours')
        .controller('MenuController', ['$cookies', 'AuthService',
            MenuController]);
}());