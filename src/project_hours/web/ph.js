(function () {
    /**
     * Login Controller using the following services:
     * @constructor
     * @param $scope
     * @param $location
     * @param $interval
     * @param $route
     * @param ProjectHoursService
     */
    function ProjectHoursController($scope, $location, $interval, $route, ProjectHoursService) {
        var self = this;
        self.debug = false;
        self.workMonth = null;
        self.workYear = null;
        self.currentDay = new Date().getDay();
        self.currentMonth = new Date().getMonth();
        self.currentYear = new Date().getFullYear();
        self.months = ['January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        self.years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025];
        self.hours = [];
        self.weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        self.weekWorkingDays = [true, true, true, true, false, false, true];
        self.days = [];
        self.projects = [];
        self.projectHours = null;
        self.totalHoursInvested = 0;
        self.daysOld = [];
        self.focusDay = null;
        self.currentTime = null;
        self.warning = {
            status: 0,
            message: ''
        };

        self.setWarning = function (received_data) {
            self.warning.status = received_data.status;
            self.warning.message = received_data.error;
            console.log(received_data.debug);
        };

        self.checkChanges = function () {
            if (!angular.equals(self.days, self.daysOld)) {
                for (var i = 0; i < self.days.length; i++)
                    for (var p = 0; p < self.days[i].projects.length; p++) {
                        if (self.days[i].projects[p].hours == 0) {
                            self.days[i].projects.splice(p, 1);
                        }
                    }
                console.log("Saving...");
                var result = ProjectHoursService.saveData(self.workMonth + 1, self.workYear, self.days);
                result.success(function (data) {
                    if (data.status == 0) {
                        angular.copy(self.days, self.daysOld);
                        self.updateTotalHoursMonth();
                    } else {
                        self.setWarning(data);
                    }
                });
                result.error(function (data) {
                    self.setWarning(data);
                });
            }
        };

        self.updateTime = function () {
            self.currentTime = new Date();
        };

        stopTime = $interval(self.checkChanges, 1000);
        stopTime = $interval(self.updateTime, 1000);

        self.daysInMonth = function (month, year) {
            return new Date(year, month, 0).getDate();
        };

        self.initHours = function () {
            return 1;
        };

        self.projectSelected = function (day) {
            for (var i = 0; i < day.projects.length; i++) {
                if (day.project.number == day.projects[i].name.number) {
                    return;
                }
            }
            day.projects.push({
                name: day.project,
                hours: self.initHours()
            });
            self.updateTotalHoursDay(day);
            self.updateTotalHoursMonth();
        };

        self.deleteProject = function (name, day) {
            for (var i = 0; i < day.projects.length; i++) {

                if (name == day.projects[i].name) {
                    day.projects.splice(i, 1);
                    self.updateTotalHoursDay(day);
                    self.updateTotalHoursMonth();
                    return;
                }
            }
        };

        self.updateTotalHoursDay = function (day) {
            var total = 0;
            for (var i = 0; i < day.projects.length; i++) {
                if (day.projects[i].hours == 0) {
                    day.projects.splice(i, 1);
                    i -= 1;
                } else {
                    total += day.projects[i].hours;
                }
            }
            day.total = total;
        };

        self.updateTotalHoursMonth = function () {
            var total = 0;
            for (var d = 0; d < self.days.length; d++) {
                if (!self.days[d].no_work)
                    total += self.days[d].total;
            }
            self.totalHoursInvested = total;
        };

        self.findMonthIndex = function (m) {
            return self.months.indexOf(m);
        };

        self.init = function () {
            var d;
            paramMonth = $route.current.params.month;
            paramYear = $route.current.params.year;

            console.log("Loading projects");
            var result = ProjectHoursService.loadProjects("currently not supported");
            result.success(function (data) {
                if (data.status == 0) {
                    self.projects = data.data;
                    self.setWarning(data);
                } else {
                    self.setWarning(data);
                }
            });

            if (!paramMonth || !paramYear) {
                self.workMonth = new Date().getMonth();
                self.workYear = new Date().getFullYear();
            } else {
                self.workMonth = parseInt(paramMonth);
                self.workYear = parseInt(paramYear);
            }
            // Let's check if already have record in database...
            console.log("Loading data...");
            result = ProjectHoursService.fillData(self.workMonth + 1, self.workYear);
            result.success(function (data) {
                if (data.status == 0) {
                    if (data.data != null)
                        self.days = data.data.days;
                    self.updateTotalHoursMonth();
                } else {
                    self.setWarning(data);
                }
            });
            result.error(function (data) {
                self.setWarning(data);
            });

            for (var i = 0; i < self.daysInMonth(self.workMonth, self.workYear); i++) {
                d = new Date(self.workYear, self.workMonth, i).getDay();
                if (self.weekWorkingDays[d] == true) {
                    self.days.push({
                        number: i + 1,
                        name: self.weekDays[d],
                        projects: [],
                        total: 0,
                        no_work: false
                    })
                } else {
                    self.days.push({
                        number: i + 1,
                        name: self.weekDays[d],
                        projects: [],
                        total: 0,
                        no_work: true
                    })
                }
            }
            for (var h = 1; h < 25; h++) {
                self.hours.push(h);
            }
            angular.copy(self.days, self.daysOld);
        };
        self.init();
    }

    angular.module('finance.projectHours')
        .controller('ProjectHoursController',
        ['$scope', '$location', '$interval', '$route', 'ProjectHoursService',
            ProjectHoursController]);
}());