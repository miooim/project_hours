(function () {
    /**
     * AuthService handles user permissions
     *
     * @param $http
     * @returns {AuthService}
     * @constructor
     */
    function ProjectHoursAdminService($http) {
        var self = this;
        self.service = {
            url:'/api/admin'
        };

        self.load = function () {
            console.log("Sending get request...");
            return $http.get(self.service.url);
        };

        self.save = function (projects) {
            return $http.put(self.service.url, projects);
        };

        return self;
    }

    angular.module('finance.projectHours')
        .service('ProjectHoursAdminService', ['$http', ProjectHoursAdminService])
}());