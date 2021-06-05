from django.db.models.fields import NullBooleanField
from django.db.models.query import NamedValuesListIterable
from django.forms.widgets import NullBooleanSelect
from app.signals import save_profile
from django.core.management.base import BaseCommand, CommandError
from app.models import *
# from django.contrib.auth.hashers import make_password, HASHERS
from django.contrib.auth.models import  User



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


    def load(self, wb, sheet_name, column_names):
        print(f'กำลัง load ... {sheet_name}')
        ws = wb[sheet_name]
        count = int(ws['A1'].value)

        print(f'count = {count}')
        data = []
        for i in range(count):  # 0,1,2,3
            # print(f'i = {i}')
            sheet_values = [
                ws[f'{chr(65+j)}{3+i}'].value for j in range(len(column_names))
            ]
            data.append(
                dict((k, v) for k, v in zip(column_names, sheet_values)))

        return data

    def handle(self, *args, **options):

        
        lenofbb = len(BloodType.objects.all())
        lenofdw = len(DaysOfWeek.objects.all())
        lenofrs = len(RaSi.objects.all())
        lenofnk = len(NakSus.objects.all())

        rasi = [[3,2,-3,0,3,-3,-1,-2,0,2,3,1],
            [1,3,2,2,-3,3,-1,-3,-2,-3,-3,0],
            [0,0,-3,-3,2,-1,3,-3,3,-3,3,2],
            [0,-2,1,3,-3,3,2,3,-2,-3,-1,3],
            [3,-1,3,1,3,1,3,2,3,-2,-1,-3],
            [0,3,2,-1,-2,3,-3,3,2,3,0,3],
            [-2,-3,-1,-3,3,-2,3,2,3,0,3,0],
            [-3,-2,2,3,1,3,0,3,-1,-2,3,-1],
            [3,3,-2,3,1,3,2,2,-2,-3,-2,-3],
            [2,3,-2,-3,-1,3,-2,-3,-1,2,2,-1],
            [3,1,3,-3,-2,0,0,0,3,2,3,1],
            [-3,-2,-2,3,1,-3,2,3,2,3,1,0]]
        range_age = [[-1,1,2,0,-2,1,-2],
            [2,0,2,-1,2,2,2],
            [2,1,0,1,2,2,1],
            [-2,-1,2,0,2,-2,0],
            [-2,-1,0,2,2,-2,-1],
            [1,0,-1,-1,2,0,-2],
            [-1,-2,0,-1,2,-2,-2]]
        bloodtype = [[2,0,1,-1],
            [1,2,2,-1],
            [1,-1,2,2],
            [-1,0,1,2]] 
        daysofweek=[[-1,0,1,-1,-1,0,-2,1],
            [-3,-1,0,1,-3,-3,-2,3],
            [-3,1,1,1,1,-3,3,3],
            [-1,3,3,3,2,-1,-2,2],
            [3,1,3,-3,-3,1,-1,-2],
            [2,2,-1,-1,-2,3,-1,-2],
            [3,-2,1,-1,-2,-2,2,0],
            [3,-3,3,0,-2,3,0,2]]
        naksus=[[-4,1,-1,3,4,3,1,-1,-1,0,0,4],
            [-4,1,1,-1,3,3,0,4,-1,1,-4,-1],
            [2,-3,-3,2,-4,4,-1,0,2,3,4,1],
            [-3,-4,1,-4,-4,-2,4,-3,0,-2,-3,2],
            [-3,2,4,1,1,2,0,0,3,-3,-4,1],
            [2,3,-3,1,4,-1,-3,-1,2,1,1,-4],
            [0,2,3,3,0,-1,3,2,4,0,2,-2],
            [-4,-3,-3,1,-4,2,2,2,2,4,3,-2],
            [1,-3,-3,-2,2,1,4,-2,-1,-3,1,-3],
            [4,0,3,2,-1,3,4,-3,-3,-3,4,-3],
            [4,-4,-1,-3,-1,-3,3,-4,-3,3,-4,3],
            [-4,-2,-4,2,-4,4,-1,1,0,0,-3,0]]
        # try:
            # pass
            
        for i in range(lenofbb):
            for j in range(lenofbb):
                if len(ScoreBloodType.objects.all()) < lenofbb*lenofbb:
                    
                    ScoreBloodType.objects.create(bloodtypeA_id=i+1,bloodtypeB_id=j+1,scorebloodtype=bloodtype[i][j])
                    print(ScoreBloodType.objects.filter(bloodtypeA_id=i+1,bloodtypeB_id=j+1,scorebloodtype=bloodtype[i][j]))
                else:
                    print("ScoreBloodType มีแล้ว")
                    print(ScoreBloodType.objects.filter(bloodtypeA_id=i+1,bloodtypeB_id=j+1,scorebloodtype=bloodtype[i][j]))

        for i in range(lenofdw):
            for j in range(lenofdw):
                if len(ScoreDaysOfWeek.objects.all()) < lenofdw*lenofdw:
                    ScoreDaysOfWeek.objects.create(daysofweekA_id=i+1,daysofweekB_id=j+1,scoredaysofweek=daysofweek[i][j])
                else:
                    print("ScoreDaysOfWeek มีแล้ว")
                    print(ScoreDaysOfWeek.objects.filter(daysofweekA_id=i+1,daysofweekB_id=j+1,scoredaysofweek=daysofweek[i][j]))
        
        for i in range(lenofnk):
            for j in range(lenofnk):
                if len(ScoreNakSus.objects.all()) < lenofnk*lenofnk:
                    ScoreNakSus.objects.create(naksusA_id=i+1,naksusB_id=j+1,scorenaksus=naksus[i][j])
                else:
                    print("ScoreNakSus มีแล้ว")
                    print(ScoreNakSus.objects.filter(naksusA_id=i+1,naksusB_id=j+1,scorenaksus=naksus[i][j]))
        
        for i in range(lenofrs):
            for j in range(lenofrs):
                if lenofrs*lenofrs > len(ScoreRaSi.objects.all()) :
                    ScoreRaSi.objects.create(rasiA_id=i+1,rasiB_id=j+1,scorerasi=rasi[i][j])
            else:
                    print(len(ScoreRaSi.objects.all()))
                    print("ScoreRaSi มีแล้ว")
                   