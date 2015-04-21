(function () {
    /**
     * AuthService handles user permissions
     *
     * @param $http
     * @returns {AuthService}
     * @constructor
     */
    function AnalysisService($http) {
        var self = this;
        self.url = '/api/analysis';

        self.getResultsByDay = function (from, to) {
            args = '?function=by_day' + '&from=' + from + '&to=' + to;
            return $http.get(self.url + args);
        };

        self.getResultsByProject = function (from, to) {
            args = '?function=by_project' + '&from=' + from + '&to=' + to;
            return $http.get(self.url + args);
        };

        return self;
    }

    angular.module('finance.projectHours')
        .service('AnalysisService', ['$http', AnalysisService])
}());