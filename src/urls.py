
from home.home_handler import HomeHandler
from project_hours.ph_hnadler import ProjectHoursHandler
from auth.login_handler import LoginHandler
from admin.ph_admin_handler import ProjectHoursAdminHandler
from analysis.analysis_hnadler import AnalysisHandler
from services.statistics.statistics_handler import StatisticsHandler

url_handlers = [
    (r'/', HomeHandler),
    (r'/api/project_hours', ProjectHoursHandler),
    (r'/api/statistics', StatisticsHandler),
    (r'/api/accounts', LoginHandler),
    (r'/api/admin', ProjectHoursAdminHandler),
    (r'/api/analysis', AnalysisHandler),
]
