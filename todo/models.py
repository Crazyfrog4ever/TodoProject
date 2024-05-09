from django.db import models
from django.contrib.auth import get_user_model




user = get_user_model()

class Todo(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    priority = models.IntegerField(default=1)
    is_done = models.BooleanField()
    user = models.ForeignKey(user, on_delete=models.CASCADE, default=1 ,related_name = 'todos')  # Replace 1 with the actual user ID




    def __str__(self):
        return f'{self.title}/ Is Done :{self.is_done}'

    class Meta:
        db_table = 'todos'
        

