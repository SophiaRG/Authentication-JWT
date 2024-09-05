def convert_db_data_in_list_dict(mycursor):
    myresult = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    list_of_dict = []
    for l in myresult:
        clothes_dictionary = {}
        for index in range(len(field_names)):
            clothes_dictionary[field_names[index]] = l[index]
        list_of_dict.append(clothes_dictionary)

    return list_of_dict