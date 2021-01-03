from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import DBConnectorSerializer, DB
from .utils import extract_info_from_request, get_db_details


@api_view(['POST'])
def result_list(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        db_info = extract_info_from_request(request.data)
        db_columns, db_details, error = get_db_details(db_info)
        if error:
            return Response({'error': error[0]}, status=error[1])
        db = DB(db_columns, db_details)
        serializer = DBConnectorSerializer(db)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
