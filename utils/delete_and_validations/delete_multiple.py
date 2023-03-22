from rest_framework.response import Response
from rest_framework import status
from json import loads




def dynamic_delete_mutiple_data(request,model,componet_name):
    reasone = request.data.get("reason")
    get_ids = request.data.get("ids")
    if get_ids is None or "" or [] or not get_ids:
        return is_valid_message(None,f"Please enter {componet_name} id's",False)
    if reasone is None or ""  or not reasone:
        return is_valid_message(None,f"Please enter {componet_name} delete reason",False)
    get_ids = loads(get_ids)
    for row in get_ids:
        data = model.objects.filter(id=row)
        if data is None or len(data) == 0:
            return is_valid_message(None,f"Selected {row} {componet_name} id is not match",False)
    data.delete()
    return is_valid_message(None,f"{componet_name} delete sucssfully",True)


def is_valid_message(seriliazer,message,serializer_Valid):
    if serializer_Valid:
        rep= {'resCode':'1','message':message}
        return Response(rep,status=status.HTTP_200_OK)
    else:
        rep= {'resCode':'0','message':message,"serializerError":seriliazer}
        return Response(rep,status=status.HTTP_200_OK)