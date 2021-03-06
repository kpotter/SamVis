import cherrypy
import simplejson
from path_obj import PathObj

class PathServer:
	
	# _cp_config = {'tools.gzip.on': True}
	
	def __init__(self):
		
		# self.path = PathObj('data/json_20130601')
		# self.path = PathObj('data/json_20130813')
		# self.path = PathObj('data/json_20130913_ex3d')
		# self.path = PathObj('data/json_20130926_imgex')
		self.path = PathObj('data/json_20130927_img_d02')
		
	@cherrypy.expose
	def index(self):
		
		return self.path.path_data_dir
		
	# ------------
	# Paths

	@cherrypy.expose
	@cherrypy.tools.gzip()
	def districtcoords(self, district_id = None, depth = 1, previous_id = None, rold = "1.0, 0.0, 0.0, 1.0"):
				
		if district_id is not None:
			dist_id = int(district_id)
			d = int(depth)
			
			if previous_id is not None:
				prev_id = int(previous_id)
			else:
				prev_id = dist_id
				
			R_old = self.parse_rold(rold)
			
			return self.path.GetDistrictDeepPathLocalRotatedCoordInfo_JSON(dist_id, prev_id, d, R_old)

	# ------------
	# Ellipses
	
	@cherrypy.expose
	@cherrypy.tools.gzip()
	def districtellipses(self, district_id = None, type = 'space', previous_id = None, rold = "1.0, 0.0, 0.0, 1.0"):
		
		if district_id is not None:
			dist_id = int(district_id)
			
			if previous_id is not None:
				prev_id = int(previous_id)
			else:
				prev_id = dist_id
				
			R_old = self.parse_rold(rold)
			
			if type == 'diffusion':
				return self.path.GetDistrictDiffusionRotatedEllipses_JSON(dist_id, prev_id, R_old)
			else:
				return self.path.GetDistrictLocalRotatedEllipses_JSON(dist_id, prev_id, R_old)

	# ------------
	# Query
	
	@cherrypy.expose
	@cherrypy.tools.gzip()
	def pathtimedistrict(self, time=None):
		
		if time is not None:
			t = int(time)
			
			# Get district ID for path at a specified time
			return self.path.GetDistrictFromPathTime_JSON(t)

	# ------------
	# Utility
	
	def parse_rold(self, rold):
		
		# Parse comma-separated list of four floats encoded as a string
		try:
			a00, a01, a10, a11 = (float(r) for r in rold.split(','))
			R_old = [[a00, a01], [a10, a11]]
		except:
			R_old = [[1.0, 0.0], [0.0, 1.0]]
		
		return R_old
			
# ------------

server_filename = '../server_example.json'
server_opts = simplejson.loads(open(server_filename).read())

cherrypy.config.update({
		# 'tools.gzip.on' : True,
		'server.socket_port': server_opts['path_port'], 
		# 'server.socket_host':'127.0.0.1'
		'server.socket_host':server_opts['server_name']
		})
cherrypy.quickstart(PathServer())
