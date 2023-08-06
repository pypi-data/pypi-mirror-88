from rest_framework.viewsets import ReadOnlyModelViewSet as DrfReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status


class ReadOnlyModelViewSet(DrfReadOnlyModelViewSet):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = {
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = {
                'data': serializer.data
            }
            return self.get_paginated_response(response)

        serializer = self.get_serializer(queryset, many=True)
        response = {
            'data': serializer.data
        }
        return Response(response)
