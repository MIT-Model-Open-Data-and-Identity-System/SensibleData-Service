from collections import defaultdict
from django.db.models import get_model
from django.forms import model_to_dict
from user_metadata.models import StaticMetadata


STATIC_METADATA = ['facebook_id', 'gender', 'starting_year']
DYNAMIC_METADATA = {'phone_number': 'UserPhoneNumber', 'study_line': 'UserStudyLine', 'status': 'UserStatus'}


def get_metadata_for_users(users, timestamp, metadata_attributes=None):
	static_attributes = [attribute for attribute in metadata_attributes if attribute in STATIC_METADATA]
	dynamic_attributes = [attribute for attribute in metadata_attributes if attribute in DYNAMIC_METADATA]
	static_metadata = get_static_metadata_for_users(users, static_attributes)
	dynamic_metadata = get_dynamic_metadata_for_users(users, timestamp, dynamic_attributes)
	metadata_dict = {}
	for user in set(static_metadata.keys()).union(set(dynamic_metadata.keys())):
		metadata_dict[user] = dict(static_metadata.get(user, {}).items() + dynamic_metadata.get(user, {}).items())

	return metadata_dict.values()


def get_static_metadata_for_users(users, static_attributes):
	metadata_dict = {}
	static_attributes.append("user")

	metadata_queryset = StaticMetadata.objects.filter(user__in=users).values(*static_attributes)

	for metadata_result in metadata_queryset:
		metadata_dict[metadata_result["user"]] = metadata_result

	return metadata_dict


def get_dynamic_metadata_for_users(users, timestamp, dynamic_attributes):
	metadata_dict = defaultdict(dict)

	for attribute in dynamic_attributes:
		dynamic_metadata_model = get_model('user_metadata', DYNAMIC_METADATA[attribute])

		metadata_queryset = dynamic_metadata_model.objects.filter(user__in=users, start_timestamp__lte=timestamp, end_timestamp__gte=timestamp)
		for metadata_result in metadata_queryset:
			metadata_dict[metadata_result.user] = dict(metadata_dict[metadata_result.user].items() + metadata_result.to_dict().items())

	return metadata_dict


class CachedMetadata(object):
	def __init__(self):
		self.static_metadata_type = None
		self.dynamic_metadata_type = None
		self.static_metadata = {}
		self.dynamic_metadata = defaultdict(list)

	def get_static_metadata(self, user, metadata_type):
		if metadata_type != self.static_metadata_type or len(self.static_metadata) == 0:
			metadata_queryset = StaticMetadata.objects.filter(user__in=user).only(metadata_type)
			for metadata_result in metadata_queryset:
				self.static_metadata[metadata_result.user] = model_to_dict(metadata_result)

		return self.static_metadata.get(user, {}).get(metadata_type, "")

	def get_dynamic_metadata(self, user, metadata_type, timestamp):
		if metadata_type != self.dynamic_metadata_type or len(self.dynamic_metadata) == 0:
			metadata_queryset = get_model('user_metadata', DYNAMIC_METADATA[metadata_type]).objects.filter(user__in=user).defer("id")
			for metadata_result in metadata_queryset:
				self.dynamic_metadata[metadata_result.user].append(model_to_dict(metadata_result))

		for metadata in self.dynamic_metadata[user]:
			if metadata["start_timestamp"] <= timestamp <= metadata["end_timestamp"]:
				return metadata.get(metadata_type, "")

		return ""





