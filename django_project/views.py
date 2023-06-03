from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from google.oauth2 import client
from googleapiclient.discovery import build
from rest_framework.views import APIView


class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = client.OAuth2WebServerFlow(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scope='https://www.googleapis.com/auth/calendar.readonly',
            redirect_uri=request.build_absolute_uri(
                reverse('calendar-redirect')))
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)


class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        flow = client.OAuth2WebServerFlow(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scope='https://www.googleapis.com/auth/calendar.readonly',
            redirect_uri=request.build_absolute_uri(
                reverse('calendar-redirect')))
        credentials = flow.step2_exchange(request.GET.get('code'))
        access_token = credentials.access_token

        service = build('calendar', 'v3', credentials=credentials)
        events = service.events().list(calendarId='primary').execute()

        # Process the list of events and return the response
        return HttpResponse(events)
