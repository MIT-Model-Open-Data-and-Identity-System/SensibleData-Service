from django.conf import settings, UserSettingsHolder
from django.test import TestCase
import MySQLdb as mdb

PROBE_NAMES = [ "dk_dtu_compute_facebook_birthday",
				"dk_dtu_compute_facebook_education",
				"dk_dtu_compute_facebook_feed",
				"dk_dtu_compute_facebook_friends",
				#"dk_dtu_compute_facebook_friendslist",
				"dk_dtu_compute_facebook_groups",
				"dk_dtu_compute_facebook_hometown",
				"dk_dtu_compute_facebook_interests",
				"dk_dtu_compute_facebook_likes",
				"dk_dtu_compute_facebook_location",
				"dk_dtu_compute_facebook_locations",
				"dk_dtu_compute_facebook_political",
				#"dk_dtu_compute_facebook_religious",
				"dk_dtu_compute_facebook_statuses",
				"dk_dtu_compute_facebook_work",
				"dk_dtu_compute_questionnaire",
			    "edu_mit_media_funf_probe_builtin_BluetoothProbe",
			   	"edu_mit_media_funf_probe_builtin_CallLogProbe",
			    "edu_mit_media_funf_probe_builtin_CellProbe",
			    "edu_mit_media_funf_probe_builtin_ContactProbe",
			    "edu_mit_media_funf_probe_builtin_HardwareInfoProbe",
			    "edu_mit_media_funf_probe_builtin_LocationProbe",
			    "edu_mit_media_funf_probe_builtin_ScreenProbe",
			    "edu_mit_media_funf_probe_builtin_SMSProbe",
			    "edu_mit_media_funf_probe_builtin_TimeOffsetProbe",
			    "edu_mit_media_funf_probe_builtin_WifiProbe",
]

TEST_DATA_DATABASE_SQL = {
	"READ_HOST": "127.0.0.1",
    "WRITE_HOST": "127.0.0.1",
	"DATABASES": {
				"dk_dtu_compute_facebook_birthday": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_education": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_feed": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_friends": "dk_dtu_compute_facebook_test",
				#"dk_dtu_compute_facebook_friendslist": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_groups": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_hometown": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_interests": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_likes": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_location": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_locations": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_political": "dk_dtu_compute_facebook_test",
				#"dk_dtu_compute_facebook_religious": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_statuses": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_facebook_work": "dk_dtu_compute_facebook_test",
				"dk_dtu_compute_questionnaire": "dk_dtu_compute_questionnaire_test",
			    "edu_mit_media_funf_probe_builtin_BluetoothProbe": "edu_mit_media_funf_probe_builtin_BluetoothProbe_test",
			   	"edu_mit_media_funf_probe_builtin_CallLogProbe": "edu_mit_media_funf_probe_builtin_CallLogProbe_test",
			    "edu_mit_media_funf_probe_builtin_CellProbe": "edu_mit_media_funf_probe_builtin_CellProbe_test",
			    "edu_mit_media_funf_probe_builtin_ContactProbe": "edu_mit_media_funf_probe_builtin_ContactProbe_test",
			    "edu_mit_media_funf_probe_builtin_HardwareInfoProbe": "edu_mit_media_funf_probe_builtin_HardwareInfoProbe_test",
			    "edu_mit_media_funf_probe_builtin_LocationProbe": "edu_mit_media_funf_probe_builtin_LocationProbe_test",
			    "edu_mit_media_funf_probe_builtin_ScreenProbe": "edu_mit_media_funf_probe_builtin_ScreenProbe_test",
			    "edu_mit_media_funf_probe_builtin_SMSProbe": "edu_mit_media_funf_probe_builtin_SMSProbe_test",
			    "edu_mit_media_funf_probe_builtin_TimeOffsetProbe": "edu_mit_media_funf_probe_builtin_TimeOffsetProbe_test",
			    "edu_mit_media_funf_probe_builtin_WifiProbe": "edu_mit_media_funf_probe_builtin_WifiProbe_test",
	}
}


def load_parameters_for_dbs_and_tables():
	parameters = []
	for probe in PROBE_NAMES:
		for table_name in ['main', 'developer', 'researcher']:
			parameters.append((probe + "." + table_name, probe, table_name))
	return parameters


class TestMySQLWrapper(TestCase):
	def setUp(self):
		self.test_connection = None
		self.saved_settings = settings.DATA_DATABASE_SQL
		setattr(settings, "DATA_DATABASE_SQL", TEST_DATA_DATABASE_SQL)

	def tearDown(self):
		if self.test_connection:
			self.test_connection.close()
		setattr(settings, "DATA_DATABASE_SQL", self.saved_settings)


