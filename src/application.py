from orm_file import Ptir, User

user = User(name="Parvez Khan", password="monkey")
user.save()

ptir = Ptir(ptir_id=1, description="None", reporter="Parvez", assignee="Itachi", status="OPEN", severity="MEDIUM")
ptir.save()
