from app.models import Member
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Message(models.Model):
    sender = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
        verbose_name = "ข้อความ:Message"

class Handler(models.Model):
    
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='member_handler', null=True, blank=True)
    rejected_m = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='rejecter', null=True, blank=True)
    reviewe_value =  models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
        
    created = models.DateTimeField(auto_now_add=True)  # When it was create
  

    def __str__(self) -> str:
        return f' {self.reviewe_value} {self.rejected_m}'

    class Meta:
        unique_together = ('member', 'rejected_m')
        verbose_name = "ตัวจัดการ:Handler"
