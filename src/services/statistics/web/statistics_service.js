(function () {
    /**
     * AuthService handles user permissions
     *
     * @param $http
     * @returns {AuthService}
     * @constructor
     */
    function StatisticsService($http) {
        var self = this;
        self.service = {
            url: '/api/statistics'
        };

        self.getMonthStatistics = function (month, year) {
            url = self.service.url + "?function=month_statistics" + "&month=" + month + "&year=" + year;
            return $http.get(url);
        };

        self.getHalfYearStatistics = function (month, year) {
            url = self.service.url + "?function=half_year_statistics" + "&month=" + month + "&year=" + year;
            return $http.get(url);
        };

        self.save = function (projects) {
            return $http.put(self.service.url, projects);
        };

        return self;
    }

    angular.module('finance.projectHours')
        .service('StatisticsService', ['$http', StatisticsService])
}());