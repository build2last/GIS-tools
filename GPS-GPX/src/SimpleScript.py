#coding:utf-8
"""
Usage

needed: gpxpy [2 3 supported]

python = 2.7
"""

from datetime import datetime, timedelta

import gpxpy
import gpxpy.gpx
import Models


def main():
	# Creating a new file:
	# --------------------

	gpx = gpxpy.gpx.GPX()

	# Create first track in our GPX:
	gpx_track = gpxpy.gpx.GPXTrack()
	gpx.tracks.append(gpx_track)

	# Create first segment in our GPX track:
	gpx_segment = gpxpy.gpx.GPXTrackSegment()
	gpx_track.segments.append(gpx_segment)

	stop_time = timedelta(seconds=180)
	cnt = 0
	with open("RawData/LGXC76C36F0050818.txt") as fr:
		fr.readline()
		first_line = fr.readline()
		item = Models.TraceLogDataItem(first_line.split(","))
		fore_time = datetime.strptime(item.collectTime, "%Y-%m-%d %H:%M:%S")
		for line in fr:
			if cnt > 1000:
				break
			item = Models.TraceLogDataItem(line.split(","))
			current_time=datetime.strptime(item.collectTime, "%Y-%m-%d %H:%M:%S")
			if (current_time - fore_time) > stop_time:
				break
			if item.vehile_status != 1 :
				continue
			gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(item.latitude, item.longitude, speed=item.speed, time=datetime.strptime(item.collectTime, "%Y-%m-%d %H:%M:%S")))
			cnt += 1
			fore_time = current_time


	print("终于")
	with open("0818.gpx", "w") as fw:
		fw.write(gpx.to_xml())

	print(u"结束了")
	print(cnt)

if __name__ == '__main__':
	main()