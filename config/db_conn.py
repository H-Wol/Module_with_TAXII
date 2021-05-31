import sqlalchemy
from ConfigManager import JsonConfigFileManager
from sqlalchemy import create_engine

db_conf = JsonConfigFileManager('db_config.json').values


engine = create_engine('{}://{}:{}@{}/{}'.format(db_config.db,db_config.host,db_config.port,db_config.user,db_config.password,db_config.database))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


db = SQLAlchemy(app)
class final_result_PE(db.Model):
    __tablename__='final_result_PE'
    num = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.VARCHAR(200))
    SHA256 = db.Column(db.String)
    MD5 = db.Column(db.String)
    filetype  = db.Column(db.VARCHAR(20))
    f_time = db.Column(db.VARCHAR(26))
    final_result = db.Column(db.String)
    LMD_result = db.Column(db.String)
    Script_result = db.Column(db.String)
    CNN_result = db.Column(db.String)
    DNN_result = db.Column(db.String)
    PE_DNN_result = db.Column(db.String)
    familyName = db.Column(db.String)
    vi_total = db.Column(db.String)
    TR_TE = db.Column(db.String)
    distance = db.Column(db.VARCHAR(50))
    Percentage = db.Column(db.VARCHAR(50))
    IP = db.Column(db.VARCHAR(16))
 
    def __init__(self, num, filename, SHA256, MD5, filetype, f_time, final_result, LMD_result, Script_result, CNN_result, DNN_result, PE_DNN_result, familyName, vi_total, TR_TE, distance, Percentage, IP):        
        self.num = num
        self.filename = filename
        self.SHA256 = SHA256
        self.MD5 = MD5
        self.filetype = filetype
        self.f_time = f_time
        self.final_result = final_result
        self.LMD_result = LMD_result
        self.Script_result = Script_result
        self.CNN_result = CNN_result
        self.DNN_result = DNN_result
        self.PE_DNN_result = PE_DNN_result
        self.familyName = familyName
        self.vi_total = vi_total
        self.TR_TE = TR_TE
        self.distance = distance
        self.Percentage = Percentage
        self.IP = IP

    
db.create_all()