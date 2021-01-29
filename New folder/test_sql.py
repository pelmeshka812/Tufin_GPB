


# jid = 41
# msg = "Generic Device ip add"
# sql = Rule(id=jid, msg= msg)
# sql.save()
# print(Rule.destination)


def req():
    p = Rule.objects.filter(id=2)
    print(p)
