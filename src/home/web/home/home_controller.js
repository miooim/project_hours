(function () {

    function HomeController($interval, ProjectHoursService, StatisticsService) {
        var self = this;
        self.debug = false;
        self.workMonth = null;
        self.workYear = null;
        self.currentDay = new Date().getDate();
        self.currentMonth = new Date().getMonth();
        self.currentYear = new Date().getFullYear();
        self.months = ['January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        self.hours = [];
        self.weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        self.days = [];
        self.today = null;
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

        self.l_labels = [];
        self.l_series = [];
        self.l_data = [];

        self.d_labels = [];
        self.d_data = [];

        self.checkChanges = function () {
            if (!angular.equals(self.days, self.daysOld)) {
                for (var i = 0; i < self.days.length; i++)
                    for (var p = 0; p < self.days[i].projects.length; p++) {
                        if (self.days[i].projects[p].hours == 0) {
                            self.days[i].projects.splice(p, 1);
                        }
                    }
                console.log("Launching save");
                var result = ProjectHoursService.saveData(self.workMonth + 1, self.workYear, self.days);
                result.success(function (data) {
                    console.log("Save success...");
                    angular.copy(self.days, self.daysOld);
                    self.halfYearStatistics();
                    self.monthStatistics();
                });
                result.error(function (data) {
                    console.log(data);
                });
            }
        };

        stopTime = $interval(self.checkChanges, 2000);

        self.updateTime = function () {
            self.currentTime = new Date();
        };

        self.daysInMonth = function (month, year) {
            return new Date(year, month, 0).getDate();
        };

        self.initHours = function () {
            return 1;
        };

        self.projectSelected = function (day) {
            console.log(day);
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
        };

        self.deleteProject = function (name, day) {
            for (var i = 0; i < day.projects.length; i++) {

                if (name == day.projects[i].name) {
                    day.projects.splice(i, 1);
                    self.updateTotalHoursDay(day);
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

        self.monthStatistics = function () {
            result = StatisticsService.getMonthStatistics(self.workMonth + 1, self.workYear);
            result.success(function (data) {
                console.log("Request month statistics");
                if (data.data) {
                    self.d_labels = data.data.labels;
                    self.d_data = data.data.hours;
                }
            });
            result.error(function (data) {
                console.log(data.data);
            });
        };

        self.halfYearStatistics = function () {
            result = StatisticsService.getHalfYearStatistics(self.workMonth + 1, self.workYear);
            result.success(function (data) {
                console.log("Request half year statistics");
                if (data.data) {
                    self.l_series = data.data.series;
                    self.l_labels = data.data.labels;
                    self.l_values = data.data.values;
                }
            });
            result.error(function (data) {
                console.log(data.data);
            });
        };

        self.updateTotalHoursMonth = function () {
            var total = 0;
            for (var d = 0; d < self.days.length; d++) {
                total += self.days[d].total;
            }
            self.totalHoursInvested = total;
        };

        self.findMonthIndex = function (m) {
            return self.months.indexOf(m);
        };

        self.init = function () {
            var d;
            var result = ProjectHoursService.loadProjects("currently not supported");
            result.success(function (data) {
                if (data.status == 0) {
                    self.projects = data.data;
                    console.log("Projects loaded");
                    console.log(self.projects)
                } else {
                    console.log("Critical error");
                    console.log(data);
                }
            });

            self.workMonth = new Date().getMonth();
            self.workYear = new Date().getFullYear();
            // Let's check if already have record in database...
            result = ProjectHoursService.fillData(self.workMonth + 1, self.workYear);
            result.success(function (result) {
                console.log(result);
                if (result.data) {
                    self.days = result.data.days;
                    angular.copy(self.days, self.daysOld);
                    self.updateTotalHoursMonth();
                    self.halfYearStatistics();
                    self.monthStatistics();
                }
            });
            result.error(function (data) {
                console.log(data);
            });

            for (var i = 0; i < self.daysInMonth(self.workMonth, self.workYear); i++) {
                d = new Date(self.workYear, self.workMonth, i).getDay();
                self.days.push({
                    number: i + 1,
                    name: self.weekDays[d],
                    projects: [],
                    total: 0
                })
            }
            for (var h = 1; h < 25; h++) {
                self.hours.push(h);
            }

            if (self.days[self.currentDay - 1].name == 'Saturday') {
                self.warning.status = -10;
                self.warning.message = 'Non working day!!!';
            }
            angular.copy(self.days, self.daysOld);
        };
        self.init();
    }

    angular.module('finance.projectHours')
        .controller('HomeController', ['$interval', 'ProjectHoursService', 'StatisticsService', HomeController]);
}());
