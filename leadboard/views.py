from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
import requests, json
from .models import Teams
from django.db.models import F

class Home(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context['teams'] = Teams.objects.all()
        return render(request, 'home.html', context)

class InitializeDB(TemplateView):
    def get(self, request):
        data = requests.get('https://s3-ap-southeast-1.amazonaws.com/he-public-data/Leaderboard_Initial_Dataset65148c7.json')
        initial_table = json.loads(data.text)
        for team in initial_table:
            if not Teams.objects.filter(team_name = team['team_name']).exists():
                team_obj = Teams()
                team_obj.team_name = team['team_name']
                team_obj.wins = int(team['wins'])
                team_obj.losses = int(team['losses'])
                team_obj.ties = int(team['ties'])
                team_obj.score = int(team['score'])
                team_obj.save()

        return redirect('home')

class Addteam(TemplateView):
    def post(self, request, *args, **kwargs):
        context = {}
        status, Message = 200, "Successfully Added"
        data = request.POST
        if not Teams.objects.filter(team_name = data['team_name']).exists():
            team_obj = Teams()
            team_obj.team_name = data['team_name']
            team_obj.save()
        else:
            status, Message = 300, "Team Name Already Exists."
        context["status"] = status
        context["Message"] = Message
        return HttpResponse(json.dumps(context))

class MatchWin(TemplateView):
    def post(self, request, *args, **kwargs):
        context = {}
        status, Message = 200, "Successfully Added Match Scores"
        data = request.POST
        winner = data['winner']
        team1 = data['team1']
        team2 = data['team2']
        team1_obj = Teams.objects.filter(team_name = team1).first()
        team2_obj = Teams.objects.filter(team_name = team2).first()
        if(winner == 'tie'):
            Teams.objects.filter(team_name = team1).update(score=team1_obj.score+1, ties=team1_obj.ties+1)
            Teams.objects.filter(team_name = team2).update(score=team2_obj.score+1, ties=team2_obj.ties+1)
        else:
            if winner == team1:
                Teams.objects.filter(team_name = team1).update(score=team1_obj.score+3, ties=team1_obj.wins+1)
                Teams.objects.filter(team_name = team2).update(ties=team2_obj.losses+1)
            else:
                Teams.objects.filter(team_name = team2).update(score=team2_obj.score+3, ties=team2_obj.wins+1)
                Teams.objects.filter(team_name = team1).update(ties=team1_obj.losses+1)

        context["status"] = status
        context["Message"] = Message
        return HttpResponse(json.dumps(context))
