from django.db import models


class TimeVariableMetadata(models.Model):
	user = models.CharField(max_length=60)
	start_timestamp = models.DateTimeField(null=True)
	end_timestamp = models.DateTimeField(null=True)

	class Meta:
		abstract = True

	def to_dict(self):
		pass


class UserPhoneNumber(TimeVariableMetadata):
	phone_number = models.CharField(max_length=100)

	def to_dict(self):
		return {"user": self.user, "phone_number": self.phone_number}


class StudyLineType(models.Model):
	study_line_name = models.CharField(max_length=100)


class UserStudyLine(TimeVariableMetadata):
	study_line = models.ForeignKey('StudyLineType')

	def to_dict(self):
		return {"user": self.user, "study_line": self.study_line.study_line_name}


class StaticMetadata(models.Model):
	user = models.CharField(max_length=60)
	facebook_id = models.CharField(max_length=100, null=True)
	gender = models.CharField(max_length=1, null=True)
	starting_year = models.IntegerField(null=True)
	first_year_exercise_group = models.CharField(max_length=100, null=True)
