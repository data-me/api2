import pytz, datetime
from .models import *
from django.http import JsonResponse


def populate(request):
    try:
        company = Group.objects.create(name='Company')
        dataScientist = Group.objects.create(name='DataScientist')

        admin = User.objects.create_user('admin', email='lennon@thebeatles.com', password='admin', is_staff=True)
        permissions = Permission.objects.all()
        for p in permissions:
            admin.user_permissions.add(p)
        data1 = User.objects.create_user(username='data1',email='data1@beatles.com',password='123456data1')
        data1.groups.add(dataScientist)

        data2 = User.objects.create_user(username='data2',email='data2@beatles.com',password='123456data2')
        data2.groups.add(dataScientist)

        company1 = User.objects.create_user(username='company1',email='company1@beatles.com',password='123456com1')
        company1.groups.add(company)

        company2 = User.objects.create_user(username='company2',email='company2@beatles.com',password='123456com2')
        company2.groups.add(company)

        dataScientist1 = DataScientist.objects.create(user = data1,name = "DataScientist 1",
        surname = "DS1",email='dataScientist1@gmail.com',
        photo='https://media.istockphoto.com/photos/smiling-man-picture-id580109640',
        address='C/Reina Mercedes Number 3',phone='628574698')

        dataScientist2 = DataScientist.objects.create(user = data2,name = "DataScientist 2",
        surname = "DS2",email='dataScientist1@gmail.com',
        photo='https://media.istockphoto.com/photos/portrait-of-a-german-businessman-with-beard-picture-id480286744',
        address='C/Cristo del Amor Number 21',phone='955766587')

        userPlan1 = UserPlan.objects.create(type='PRO',dataScientist=dataScientist1,startDate=datetime.datetime(2019,1,1,0,0,0,0,pytz.UTC),expirationDate=datetime.datetime(2020,1,1,0,0,0,0,pytz.UTC))

        company01 = Company.objects.create(user = company1, name = 'Company 1', description = 'Description 1',nif = 'nif1', logo = 'www.company1.com')
        company02 = Company.objects.create(user = company2, name = 'Company 2', description = 'Description 2',nif = 'nif2', logo = 'www.company2.com')

        offer1 = Offer.objects.create(title='Offer1',description='this is the offer 1',price_offered =1000,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2019,7,12,21,0,0,0,pytz.UTC), finished = False, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile1.csv',company= company01)
        offer2 = Offer.objects.create(title='Offer2',description='this is the offer 2',price_offered =1350,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2019,4,1,10,0,0,0,pytz.UTC), finished = True, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile2.csv',company= company01)
        offer3 = Offer.objects.create(title='Offer3',description='this is the offer 3',price_offered =3100,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2019,9,12,10,0,0,0,pytz.UTC), finished = False, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile3.csv',company= company01)
        offer4 = Offer.objects.create(title='Offer4',description='this is the offer 4',price_offered =200,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2019,9,12,10,0,0,0,pytz.UTC), finished = False, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile4.csv',company= company02)
        offer5 = Offer.objects.create(title='Offer5',description='this is the offer 5',price_offered =450,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2020,3,2,10,0,0,0,pytz.UTC), finished = False, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile5.csv',company= company02)

        apply1 = Apply.objects.create(title='Apply1',description='this is the apply 1',
                                      date=datetime.datetime(2019,3,27,16,30,0,0,pytz.UTC),status='RE',dataScientist = dataScientist2, offer = offer2)
        apply2 = Apply.objects.create(title='Apply2',description='this is the apply 2',
                                      date=datetime.datetime(2019,3,28,23,13,0,0,pytz.UTC),status='AC',dataScientist = dataScientist1,offer = offer2)
        apply3 = Apply.objects.create(title='Apply3',description='this is the apply 3',
                                      date=datetime.datetime(2019,4,1,23,13,0,0,pytz.UTC),status='PE',dataScientist = dataScientist1,offer = offer3)
        apply4 = Apply.objects.create(title='Apply4',description='this is the apply 4',
                                      date=datetime.datetime(2019,4,1,12,0,0,0,pytz.UTC),status='PE',dataScientist = dataScientist2,offer = offer1)

        apply5 = Apply.objects.create(title='Apply5',description='this is the apply 5',
                                      date=datetime.datetime(2019,4,1,12,0,0,0,pytz.UTC),status='AC',dataScientist = dataScientist1,offer = offer5)

        submit1 = Submition.objects.create(dataScientist = dataScientist1, offer = offer2, file = 'https://github.com/data-me/api2/blob/Sprint2/submissionfile1.csv',comments = 'Here is a test pdf to check the Submition with an accepted status',status = 'AC')
        submit2 = Submition.objects.create(dataScientist = dataScientist1, offer = offer5, file = 'https://github.com/data-me/api2/blob/Sprint2/submissionfile2.csv',comments = 'Here is a test pdf to check the Submition with a SUBMITTED Status',status = 'SU')


        cv1 = CV.objects.create(owner = dataScientist1)
        cv2 = CV.objects.create(owner = dataScientist2)

        sectionName1 = Section_name.objects.create(name = 'Educational Record')
        sectionName2 = Section_name.objects.create(name = 'Professional Record')
        sectionName3 = Section_name.objects.create(name = 'Personal Record')

        section1 = Section.objects.create(name = sectionName1,cv = cv1 )
        section2 = Section.objects.create(name = sectionName3,cv = cv1 )
        section3 = Section.objects.create(name = sectionName2,cv = cv2 )
        section4 = Section.objects.create(name = sectionName2,cv = cv1 )

        item1 = Item.objects.create(name='Studient in the US', section=section1, description='I studied in the ETSII, US for 4 years. It was a hard work',
                                    entity = 'ETSII - US',date_start=datetime.datetime(2014,3,28,23,13,0,0,pytz.UTC), date_finish= datetime.datetime(2019,6,28,23,13,0,0,pytz.UTC))

        item2 = Item.objects.create(name='About me', section=section2, description="I'm a good partner. I can work with others DataScientist if you need. I work very fast and i can finish any work",
                                    entity ='Me',date_start=datetime.datetime(1997,1,18,23,13,0,0,pytz.UTC), date_finish= datetime.datetime(2019,6,28,23,13,0,0,pytz.UTC))

        item3 = Item.objects.create(name='Working in Everis', section=section4, description="I am working in Everis procesing data from users.",
                                    entity ='',date_start=datetime.datetime(2015,11,29,21,13,0,0,pytz.UTC),
                                     date_finish= None)

        item4 = Item.objects.create(name='Engineer in Endesa', section=section3, description="I've work in Endesa since 2013. I was in charge the data from the bills.",
                                    entity = 'Ensesa',date_start=datetime.datetime(2013,3,11,23,13,0,0,pytz.UTC), date_finish= datetime.datetime(2017,1,2,23,13,0,0,pytz.UTC))

        message1 = Message.objects.create(receiver = data1, sender = admin, title = "Welcome!", body= "Welcome to DataMe!", isAlert=False)
        message2 = Message.objects.create(receiver = data2, sender = admin, title = "Welcome!", body= "Welcome to DataMe!", isAlert=False)
        message3 = Message.objects.create(receiver = company1, sender = admin, title = "Welcome!", body= "Welcome to DataMe!", isAlert=False)
        message4 = Message.objects.create(receiver = company2, sender = admin, title = "Welcome!", body= "Welcome to DataMe!", isAlert=False)

        return JsonResponse({'message': 'DB populated'})
    except Exception as e:
        return JsonResponse({'Error': 'DB already populated ' + str(e)})
