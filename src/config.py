from tornado.options import define, options


define('mongodb', default='localhost:27017', help='mongodb host name or ip address +port', type=str)
define('mongod_name', default='project_hours', help='Project hours database name', type=str)
define('auth_db', default='project_hours', help='authentication database', type=str)
define('auth_driver', default='auth.ldap_auth.LdapAuth', help='authentication driver', type=str)
define('app_port', default=8181, help='application port', type=int)

# LDAP authentication
define("active_directory_server", default='server_name', help="Active directory server", type=str)
define("active_directory_username", default='user_name', help="Active directory username", type=str)
define("active_directory_password", default='password', help="Active directory password", type=str)
define("active_directory_search_def", default='ou=Crow,dc=Crow,dc=local', help="active directory search definition",
       type=str)

#user cookie
define("auth_cookie_name", default='project_hours', help="name of the cookie to use for authentication", type=str)
