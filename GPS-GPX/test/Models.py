#coding:utf-8
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

"""基本对象"""



class Location:
	def __init__(self, kward):
		self.name = "-".join(kward[0:-4])
		self.latitude = float(kward[-4])
		self.longitude = float(kward[-3])
		self.type = kward[-2]
		self.typeid = int(kward[-1])

	def to_dic(self):
		d = {"name":self.name.replace("'",""), "latitude":self.latitude, "longitude":self.longitude,
		"type":self.type,"typeid":self.typeid}
		return d


def args_generator(args):
	count = 0
	length = len(args)
	while count < length:
		yield args[count]
		count += 1

class TraceLogDataItem:
	def __init__(self, args_ge):
		if len(args_ge) > 1:
			self.raw_line = ",".join(args_ge)
			args_ge = args_generator(args_ge)
		else:
			return None
		self.collectTime = next(args_ge)
		self.total_mileage = next(args_ge)
		self.longitude_flag = next(args_ge)
		self.alm_motor_controller_temperature = next(args_ge)
		self.alm_drive_motor_temperature = next(args_ge)
		self.alm_motor_driving_system_fault = next(args_ge)
		self.alm_dcdc_temperature = next(args_ge)
		self.alm_dcdc_state = next(args_ge)
		self.alm_total_voltage_battery_pack = next(args_ge)
		self.alm_single_pack_maximum_temperature = next(args_ge)
		self.alm_single_pack_minimum_temperature = next(args_ge)
		self.alm_single_pack_maximum_voltage = next(args_ge)
		self.alm_single_pack_minimum_voltage = next(args_ge)
		self.alm_high_pressure_interlock_state = next(args_ge)
		self.alm_value_of_insulation_resistance = next(args_ge)
		self.alm_collision_signal_state = next(args_ge)
		self.alm_energy_storage_system_fault = next(args_ge)
		self.alm_ABS_system_fault = next(args_ge)
		self.positioning_state = next(args_ge)
		self.latitude_flag = next(args_ge)
		self.longitude = float(next(args_ge))/1000000
		self.latitude = float(next(args_ge))/1000000
		self.speed = next(args_ge)
		self.direction = next(args_ge)
		self.motor_controlling_temperature = next(args_ge)
		self.drive_motor_speed = next(args_ge)
		self.drive_motor_temperature = next(args_ge)
		self.motor_bus_current = next(args_ge)
		self.accelerator_pedal_stroke = next(args_ge)
		self.brake_pedal_state = next(args_ge)
		self.power_system_ready = next(args_ge)
		self.urgent_cut_off_power_request = next(args_ge)
		self.high_voltage_current_of_battery = next(args_ge)
		self.soc = next(args_ge)
		self.residual_energy = next(args_ge)
		self.total_battery_voltage = next(args_ge)
		self.single_pack_maximum_temperature = next(args_ge)
		self.single_pack_minimum_temperature = next(args_ge)
		self.single_pack_maximum_voltage = next(args_ge)
		self.single_pack_minimum_voltage = next(args_ge)
		self.value_of_insulation_resistance = next(args_ge)
		self.battery_equalization_activation = next(args_ge)
		self.max_temperature_battery_pack = next(args_ge)
		self.min_temperature_battery_pack = next(args_ge)
		self.start_time = next(args_ge)
		self.liquid_fuel_consumption = next(args_ge)
		self.status = next(args_ge)
		self.end_time = next(args_ge)
		self.vehile_status = int(next(args_ge).strip()) # 0：停止；1：行驶；2：充电

	def get_raw_line(self):
		return self.raw_line.strip()


class RegionBlock:
	def __init__(self, from_latitude, to_latitude,
		from_longitude, to_longitude, tags=[]):
		self.from_longitude = from_longitude
		self.to_longitude = to_longitude
		self.from_latitude = from_latitude
		self.to_latitude = to_latitude
		self.tags = tags

	def inlude(self, longitude, latitude):
		return (longitude < self.to_longitude and longitude > self.from_latitude and
			latitude < self.to_latitude and latitude > self.from_latitude)


SEGMENT_INCREMENT = 0.03

class LocaDiv(object):
    # 构造函数，传入需要划分的坐标
    def __init__(self, loc_all):
        self.loc_all = loc_all

    # 定义函数，以0.05度为间隔，对维度进行划分，返回一个列表
    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        lat_list = []
        for i in range(0, int((lat_ne - lat_sw + 0.0001) / SEGMENT_INCREMENT)):
            lat_list.append(lat_sw + SEGMENT_INCREMENT * i)
        lat_list.append(lat_ne)
        return lat_list

    # 定义函数，以0.05度为间隔，对经度进行划分，返回一个列表
    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = []
        for i in range(0, int((lng_ne - lng_sw + 0.0001) / SEGMENT_INCREMENT)):
            lng_list.append(lng_sw + SEGMENT_INCREMENT * i)
        lng_list.append(lng_ne)
        return lng_list
        # 定义函数，将经纬度进行组合，返回一个列表

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = a + ',' + b
                ab_list.append(ab)
        return ab_list

    # 定义函数，将对角线坐标进行组合，返回一个列表
    def ls_row(self):
        # type: () -> object
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        ls = []
        for n in range(0, len(l1) - 1):
            for i in range(0 + (len(l1) + 1) * n, len(l2) + (len(l2)) * n - 1):
                a = ls_com_v[i]
                b = ls_com_v[i + len(l2) + 1]
                ab = a + ',' + b
                ls.append(ab)
        return ls


# 上海市地处东经120度51分至122度12分,北纬30度40分至31度53分之间
def load_poi_data(poi_file):
	poi_dir = {}
	with open(poi_file) as fr:
		for item in fr:
			fr.split(",")


from math import radians, cos, sin, asin, sqrt  
  
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数  
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 

    The units are in meters
    """  
    # 将十进制度数转化为弧度  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
  
    # haversine公式  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里  
    return c * r * 1000  


def main(file_path):
	#import inspect
	with open(file_path) as f:
		lines = f.readlines()
		for line in lines[:5]:
			item = DataItemBYD(args_generator(line.split(",")))
			# print(inspect.getmembers(item))

if __name__ == '__main__':
	main("data.txt")