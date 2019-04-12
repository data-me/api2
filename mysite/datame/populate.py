import pytz, datetime
from .models import *
from django.http import JsonResponse


def populate(request):
    try:
        company = Group.objects.create(name='Company')
        dataScientist = Group.objects.create(name='DataScientist')

        admin = User.objects.create_user('admin', email='admin@datame.com', password='admin', is_staff=True)
        permissions = Permission.objects.all()
        for p in permissions:
            admin.user_permissions.add(p)
        data1 = User.objects.create_user(username='data1',email='data1@datame.com',password='123456data1')
        data1.groups.add(dataScientist)

        data2 = User.objects.create_user(username='data2',email='data2@datame.com',password='123456data2')
        data2.groups.add(dataScientist)

        company1 = User.objects.create_user(username='company1',email='company1@datame.com',password='123456com1')
        company1.groups.add(company)

        company2 = User.objects.create_user(username='company2',email='company2@datame.com',password='123456com2')
        company2.groups.add(company)

        dataScientist1 = DataScientist.objects.create(user = data1,name = "Jonh",
        surname = "Doe",email='dataScientist1@gmail.com',
        photo='https://media.istockphoto.com/photos/smiling-man-picture-id580109640',
        address='C/Reina Mercedes Number 3',phone='628574698')

        dataScientist2 = DataScientist.objects.create(user = data2,name = "Jack",
        surname = "Smith",email='dataScientist1@gmail.com',
        photo='https://media.istockphoto.com/photos/portrait-of-a-german-businessman-with-beard-picture-id480286744',
        address='C/Cristo del Amor Number 21',phone='955766587')

        userPlan1 = UserPlan.objects.create(type='PRO',dataScientist=dataScientist1,startDate=datetime.datetime(2019,1,1,0,0,0,0,pytz.UTC),expirationDate=datetime.datetime(2020,1,1,0,0,0,0,pytz.UTC),isPayed=True)

        company01 = Company.objects.create(user = company1, name = 'Endesa', description = 'Endesa, fundada como «Empresa Nacional de Electricidad Sociedad Anónima» y cuyo nombre legal es Endesa, S.A., es una empresa española que opera en los sectores eléctrico y gasístico.',nif = '44060644A', logo = 'https://graffica.info/wp-content/uploads/2016/01/Captura-de-pantalla-2016-01-28-a-las-19.00.55.png')
        company02 = Company.objects.create(user = company2, name = 'Everis', description = 'Somos everis an NTT DATA Company, nos dedicamos a la consultoría y outsourcing abarcando todos los sectores del ámbito económico, llegando a facturar en el último ejercicio fiscal cerca de 1.173 millones de euros.',nif = '45070745B', logo = 'https://worldfootballsummit.com/wp-content/uploads/2018/08/logo-vector-everis.jpg')

        offer1 = Offer.objects.create(title='Consumo de luz medio 2018',description='Se necesita el tratamiento de los datos del consumo de luz en España en el año 2018.',price_offered =1000,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2019,7,12,21,0,0,0,pytz.UTC), finished = False, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile1.csv',contract="Debe comprometerse a entregarlo a tiempo",company= company01)
        offer2 = Offer.objects.create(title='Consumo de luz medio 2017',description='tSe necesita el tratamiento de los datos del consumo de luz en España en el año 2017.',price_offered =1350,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2019,4,1,10,0,0,0,pytz.UTC), finished = True, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile2.csv',contract="Los datos se deben tratar con la mayor confidencialidad",company= company01)
        offer3 = Offer.objects.create(title='Consumo de luz medio 2016',description='Se necesita el tratamiento de los datos del consumo de luz en España en el año 2016.',price_offered =3100,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2019,9,12,10,0,0,0,pytz.UTC), finished = False, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile3.csv',contract="Los datos se deben tratar con la mayor confidencialidad",company= company01)
        offer4 = Offer.objects.create(title='Uso medio de Chrome en 2018',description='Se necesita el tratamiento de los datos del uso medio de Google Chrome en el año 2018.',price_offered =200,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2019,9,12,10,0,0,0,pytz.UTC), finished = False, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile4.csv',contract="Debe comunicarse actualizaciones diarias por mensaje de la aplicacion",company= company02)
        offer5 = Offer.objects.create(title='Uso medio de Firefox en 2018',description='Se necesita el tratamiento de los datos del uso medio de Mozilla Firefox en el año 2018.',price_offered =450,
                                      creation_date=datetime.datetime.utcnow(),limit_time = datetime.datetime(2020,3,2,10,0,0,0,pytz.UTC), finished = False, files = 'https://github.com/data-me/api2/blob/Sprint2/offerfile5.csv',contract="No puede difundir los datos",company= company02)

        apply1 = Apply.objects.create(title='Propuesta de Jack Smith para Luz 2017',description='Mi propuesta consiste en el uso de métodos que Machine Learning no permite',
                                      date=datetime.datetime(2019,3,27,16,30,0,0,pytz.UTC),status='RE',dataScientist = dataScientist2, offer = offer2)
        apply2 = Apply.objects.create(title='Propuesta de John Doe para Luz 2017',description='Mi propuesta consiste en el uso de Machine Learning',
                                      date=datetime.datetime(2019,3,28,23,13,0,0,pytz.UTC),status='AC',dataScientist = dataScientist1,offer = offer2)
        apply3 = Apply.objects.create(title='Propuesta de John Doe para Luz 2016',description='Mi propuesta consiste en el uso de Machine Learning',
                                      date=datetime.datetime(2019,4,1,23,13,0,0,pytz.UTC),status='PE',dataScientist = dataScientist1,offer = offer3)
        apply4 = Apply.objects.create(title='Propuesta de Jack Smith para Luz 2018',description='Mi propuesta consiste en el uso de métodos que Machine Learning no permite',
                                      date=datetime.datetime(2019,4,1,12,0,0,0,pytz.UTC),status='PE',dataScientist = dataScientist2,offer = offer1)

        apply5 = Apply.objects.create(title='Propuesta de John Doe para Firefox 2018',description='Mi propuesta consiste en el uso de Machine Learning',
                                      date=datetime.datetime(2019,4,1,12,0,0,0,pytz.UTC),status='AC',dataScientist = dataScientist1,offer = offer5)

        submit1 = Submition.objects.create(dataScientist = dataScientist1, offer = offer2, file = 'https://github.com/data-me/api2/blob/Sprint2/submissionfile1.csv',comments = 'Se realizó correctamente y antes del tiempo estimado.',status = 'AC')
        submit2 = Submition.objects.create(dataScientist = dataScientist1, offer = offer5, file = 'https://github.com/data-me/api2/blob/Sprint2/submissionfile2.csv',comments = 'Se ha invertido algo mas de tiempo del ideal estimado',status = 'SU')


        cv1 = CV.objects.create(owner = dataScientist1)
        cv2 = CV.objects.create(owner = dataScientist2)

        sectionName1 = Section_name.objects.create(name = 'Formación educacional')
        sectionName2 = Section_name.objects.create(name = 'Formación profesional')
        sectionName3 = Section_name.objects.create(name = 'Habilidades personales')

        section1 = Section.objects.create(name = sectionName1,cv = cv1 )
        section2 = Section.objects.create(name = sectionName3,cv = cv1 )
        section3 = Section.objects.create(name = sectionName2,cv = cv2 )
        section4 = Section.objects.create(name = sectionName2,cv = cv1 )

        item1 = Item.objects.create(name='Estudiante en la US', section=section1, description='Estudié en la ETSII, US durante 4 años de duro trabajo',
                                    entity = 'ETSII - US',date_start=datetime.datetime(2014,3,28), date_finish= datetime.datetime(2019,6,28))

        item2 = Item.objects.create(name='Sobre mí', section=section2, description="Soy un buen compañero, puedo trabajar de forma cooperativa sin problemas.",
                                    entity ='Yo',date_start=datetime.datetime(1997,1,18), date_finish= datetime.datetime(2019,6,28))

        item3 = Item.objects.create(name='Trabajando en Everis', section=section4, description="Estoy actualmente trabajando en Everis procesando datos de los usuarios.",
                                    entity ='',date_start=datetime.datetime(2015,11,29),
                                     date_finish= None)

        item4 = Item.objects.create(name='Ingeniero en Endesa', section=section3, description="He trabajado en Endesa a cargo de los datos de las facturas.",
                                    entity = 'Ensesa',date_start=datetime.datetime(2013,3,11), date_finish= datetime.datetime(2017,1,2))

        message1 = Message.objects.create(receiver = data1, sender = admin, title = "Welcome!", body= "Welcome to DataMe!", isAlert=False)
        message2 = Message.objects.create(receiver = data2, sender = admin, title = "Welcome!", body= "Welcome to DataMe!", isAlert=False)
        message3 = Message.objects.create(receiver = company1, sender = admin, title = "Welcome!", body= "Welcome to DataMe!", isAlert=False)
        message4 = Message.objects.create(receiver = company2, sender = admin, title = "Welcome!", body= "Welcome to DataMe!", isAlert=False)

        return JsonResponse({'message': 'DB populated'})
    except Exception as e:
        return JsonResponse({'Error': 'DB already populated ' + str(e)})
