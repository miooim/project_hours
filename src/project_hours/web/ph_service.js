(function () {
    /**
     * AuthService handles user permissions
     *
     * @param $http
     * @returns {AuthService}
     * @constructor
     */
    function ProjectHoursService($http) {
        var self = this;
        self.url = '/api/project_hours';

        self.fillData = function (month, year) {
            args = '?month=' + month + '&year=' + year;
            return $http.get(self.url + args);
        };

        self.loadProjects = function (group) {
            args = '?group=' + group;
            return $http.get(self.url + args);
        };

        self.saveData = function (month, year, days) {
            args = '?month=' + month + '&year=' + year;
            return $http.put(self.url + args, days);
        };

        return self;
    }

    angular.module('finance.projectHours')
        .service('ProjectHoursService', ['$http', ProjectHoursService])
}());