def get_response_object(req):
	res_lst = []

	for item in req:
		res_lst.append(item.to_mongo())

	return res_lst
