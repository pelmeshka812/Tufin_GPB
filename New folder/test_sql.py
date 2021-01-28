from core.models import Rule

jid = 41
msg = "Generic Device ip add"
sql = Rule(id=jid, msg= msg)
sql.save()
print(Rule.destination)