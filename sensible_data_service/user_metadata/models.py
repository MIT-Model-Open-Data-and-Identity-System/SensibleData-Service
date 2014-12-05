from django.db import models


class TimeVariableMetadata(models.Model):
	user = models.CharField(max_length=60)
	start_timestamp = models.DateTimeField(null=True)
	end_timestamp = models.DateTimeField(null=True)

	class Meta:
		abstract = True


class UserPhoneNumber(TimeVariableMetadata):
	phone_number = models.CharField(max_length=100)


class StudyLineType(models.Model):
	study_line_name = models.CharField(max_length=100)


class UserStudyLine(TimeVariableMetadata):
	study_line = models.ForeignKey('StudyLineType')


class StaticMetadata(models.Model):
	user = models.CharField(max_length=60)
	facebook_id = models.CharField(max_length=100, null=True)
	gender = models.CharField(max_length=1)
	starting_year = models.IntegerField()
