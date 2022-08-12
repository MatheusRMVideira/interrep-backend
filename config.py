APPLICATION_PREFIX = "/api"

JWT_KEY = "14834c55af7e2ca2adda98495f6e64a2cc032cb7"

JWT_LIFETIME = 3600*24*180 #seconds

#Localhost
DATABASE_URI = "mysql+pymysql://root:123456@localhost/interrep"

#Heroku
#DATABASE_URI = 
PASSWORD_MIN_LENGTH = 6

PASSWORD_MAX_LENGTH = 50

UPLOAD_FOLDER = './images'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

MAX_CONTENT_LENGTH = 2 * 1024 * 1024

PERMISSIONS_REQUIRED = {
    'CreateRepublic':['create_rep'],
    'CreatePlayer':['create_player'],
    'ModifyRepublic':['modify_rep'],
    'ModifyPlayer':['modify_player'],
    'DeleteRepublic':['delete_rep'],
    'DeletePlayer':['delete_player'],
    'ToggleMarket':['toggle_market'],
    'SetDeadline':['toggle_market'],
    'GivePlayerPoints':['modify_player'],
    'CreateGame':['create_game'],
    'UpdateGame':['update_game'],
    'DeleteGame':['delete_game'],
    'GivePlayersScore':['modify_player'],
    'BenchPlayer':['modify_player']
    }
