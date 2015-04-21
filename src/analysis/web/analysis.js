(function () {
    /**
     * Login Controller using the following services:
     * @constructor
     * @param $scope
     * @param $location
     * @param $interval
     * @param $filter
     * @param AnalysisService
     */
    function AnalysisController($scope, $location, $interval, $filter, AnalysisService) {
        var self = this;
        self.debug = false;
        self.weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        self.weekWorkingDays = [true, true, true, true, false, false, true];
        self.currentTime = null;
        self.warning = {
            status: 0,
            message: ''
        };

        self.tableData = [{
            from: false,
            to: false,
            dateFrom: '',
            dateTo: '',
            data: [],
            gs: '',
            filename: 'ProjectsSummary_' + $filter('date')(new Date(), "yyyymmddhhMM") + '.csv',
            headers: ['Project', 'Total hours']
        }, {
            from: false,
            to: false,
            dateFrom: '',
            dateTo: '',
            data: [],
            gs: '',
            filename: 'ByDaySummary_' + $filter('date')(new Date(), "yyyymmddhhMM") + '.csv',
            headers: ['Day of week', 'Day', 'Month', 'User' ,'Year', 'Hours']
        }];
        self.tab = '';

        self.tabSet = function(who){
            self.tab = who;
        };

        self.setWarning = function (received_data) {
            self.warning.status = received_data.status;
            self.warning.message = received_data.error;
            console.log(received_data.debug);
        };

        self.datePickerOpen = function ($event, which) {
            console.log("Event sent...");
            $event.preventDefault();
            $event.stopPropagation();
            if (which == 'to')
                self.tableData[self.tab].to = true;
            if (which == 'from')
                self.tableData[self.tab].from = true;
        };

        self.getResults = function () {
            if (self.tab == 0){
                result = AnalysisService.getResultsByProject($filter('date')(self.tableData[self.tab].dateFrom,
                        'dd MMM yyyy'), $filter('date')(self.tableData[self.tab].dateTo, 'dd MMM yyyy'));
            } else if (self.tab == 1){
                result = AnalysisService.getResultsByDay($filter('date')(self.tableData[self.tab].dateFrom,
                        'dd MMM yyyy'), $filter('date')(self.tableData[self.tab].dateTo, 'dd MMM yyyy'));
            }
            result.success(function (data) {
                console.log(data);
                self.tableData[self.tab].data = data.data;
            });
            result.error(function (data) {
                console.log(data);
            })
        };

        self.getExportArray = function(){
            return self.tableData[self.tab].data;
        };

        self.init = function () {

        };
        self.init();
    }

    angular.module('finance.projectHours')
        .controller('AnalysisController',
        ['$scope', '$location', '$interval', '$filter', 'AnalysisService',
            AnalysisController]);
}());