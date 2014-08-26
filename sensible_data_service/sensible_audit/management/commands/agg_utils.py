from datetime import datetime, timedelta
import re

def date_is_valid(level, date):
	if level == 'day':
		try:
			return datetime.strptime(date, '%Y/%m/%d')
		except ValueError, e:
			print 'Date is not valid (YYYY/mm/dd)'
			return False
	elif level == 'week':
		return parse_week(date)
	return False

def parse_week(date):
	match = re.match(r'(\d{4})/(\d{1,2})', date)
	if match:
		year = int(match.group(1))
		week_num = int(match.group(2))
		if week_num > int(datetime(year, 12, 31).strftime('%W')):
			raise ValueError('Week date [%s] format not correct (YYYY/dd)' % date)
		count = 0
		for week in weeks_of_year(year):
			if count == week_num: return week
			count += 1
		return week
	else:
		raise ValueError('Week date [%s] format not correct (YYYY/dd)' % date)
		return False

def weeks_of_year(year):
	'''
	Returns an iterator with all the weeks of the given year.
	'''
	jan_1st = datetime(year, 1, 1)
	dec_31st = datetime(year, 12, 31)
	for week in range(0, int(dec_31st.strftime('%W'))):
		yield jan_1st + timedelta(week * 7)