import mongoengine as me
from mongoengine import Document

me.connect("test")

class Ptir(Document):
	ptir_id = me.IntField(required=True, primary_key=True)
	description = me.StringField(required=True)
	created_on = me.StringField()
	modified_on = me.StringField()
	created_by = me.StringField()
	modified_by = me.StringField()
	reporter = me.StringField(required=True)
	assignee = me.StringField(required=True)
	status = me.StringField(required=True)
	severity = me.StringField(required=True)
	release = me.StringField()

class User(Document):
	name = me.StringField(required=True, primary_key=True)
	password = me.StringField(required=True)
	email = me.StringField()
	role = me.StringField()
	ptirs_assigned = me.StringField()
