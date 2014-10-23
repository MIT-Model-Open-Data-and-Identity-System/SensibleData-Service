from django.db import models


class TimeVariableMetadata(models.Model):
	start_timestamp = models.DateTimeField(null=True)
	end_timestamp = models.DateTimeField(null=True)


class StatusType(models.Model):
	status_label = models.CharField(max_length=100)


class UserStatus(TimeVariableMetadata):
	status = models.ManyToManyField(StatusType)


class UserPhoneNumber(TimeVariableMetadata):
	phone_number = models.CharField(max_length=100)


class StudyLineType(models.Model):
	study_line_name = models.CharField(max_length=100)


class UserStudyLine(TimeVariableMetadata):
	study_line = models.ManyToOneRel(StudyLineType, "study_line_name")


class UserMetadata(models.Model):
	user = models.CharField(max_length=100)
	facebook_id = models.CharField(max_length=100, null=True)
	study_line = models.ManyToManyField(UserStudyLine, null=True)
	current_status = models.ManyToManyField(UserStatus)
	phone_number = models.ManyToManyField(UserPhoneNumber, null=True)