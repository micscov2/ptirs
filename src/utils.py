import os

def get_response_object(req):
	res_lst = []

	for item in req:
		res_lst.append(item.to_mongo())

	return res_lst


def check_file_present(filepath):
    return os.path.exists(filepath)    


def check_all_files_present(filepaths):
    return all(check_file_present(filepath) for filepath in filepaths)
