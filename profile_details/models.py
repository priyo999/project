from django.db import models

# Create your models here.

class CandidateDetails(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null= True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'candidate_details'

class Skills(models.Model):
    candidate = models.ForeignKey(CandidateDetails, related_name='candidate_skill',
                             on_delete=models.CASCADE,blank=True,null=True)
    skill = models.CharField(max_length=50, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'skills'

