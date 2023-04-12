import datetime
now = datetime.datetime.now()
print("Now is ", now.strftime("%d-%m_%Y"), " at ", now.strftime("%H:%M"))
print("or, to be more precise, %s" % now)
