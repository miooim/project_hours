(function () {
    /**
     * Login Controller using the following services:
     * @constructor
     * @param $filter
     * @param $interval
     * @param ProjectHoursAdminService
     */
    function ProjectHoursAdminController($filter, $interval, ProjectHoursAdminService) {
        var self = this;
        self.projects = [];
        self.oldProjects = [];
        self.requestStatus = {
            status: 0,
            description: ''
        };

        self.addProjectItem = function () {
            self.projects.push({
                number: 0,
                name: '',
                description: ''
            })
        };

        self.smartSave = function () {
            console.log("Timer triggered");
            if (!angular.equals(self.projects, self.oldProjects)) {
                console.log("Save triggered");
                var result = ProjectHoursAdminService.save(self.projects);
                self.oldProjects = angular.copy(self.projects);
                result.success(function (data) {
                    if (data.status != 0) {
                        console.log(data.debug);
                        self.requestStatus.message = data.error;
                        self.requestStatus.status = data.status;
                    }
                });
                result.error(function (data) {
                    console.log(data.debug);
                    self.requestStatus.message = data.error;
                    self.requestStatus.status = data.status;
                })
            }
        };

        $interval(self.smartSave(), 1000);

        self.deleteProjectItem = function (project) {
            for (var i = 0; i < self.projects.length; i++) {
                if (angular.equals(project, self.projects[i])) {
                    self.projects.splice(i, 1);
                    return;
                }
            }
        };

        self.sortProjectItems = function () {
            var orderBy = $filter('orderBy');
            result = orderBy(self.projects, '+number', false);
            self.projects = angular.copy(result);
        };

        self.cleanWarning = function () {
            self.requestStatus.status = 0;
            self.requestStatus.message = '';
        };

        self.init = function () {
            console.log("Inititalizing...");
            var result = ProjectHoursAdminService.load();
            result.success(function (data) {
                if (data.data != null)
                    self.projects = angular.copy(data.data);
                else {
                    self.projects = [];
                    console.log(data.debug);
                    self.requestStatus.message = data.error;
                    self.requestStatus.status = data.status;
                }
            });
            result.error(function (data) {
                console.log(data.debug);
                self.requestStatus.message = data.error;
                self.requestStatus.status = data.status;
            });
        };

        self.init();

    }

    angular.module('finance.projectHours')
        .controller('ProjectHoursAdminController', ['$filter', '$interval', 'ProjectHoursAdminService',
            ProjectHoursAdminController]);
}());