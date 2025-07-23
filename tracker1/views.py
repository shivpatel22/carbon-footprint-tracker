from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import UserProfile
from .models import ActivityLog
from .forms import ActivityLogForm
from django.contrib.auth.decorators import login_required
from .models import UploadRecord
from .forms import UploadForm
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import ProfilePictureForm


@login_required
def edit_activity(request, log_id):
    log = get_object_or_404(ActivityLog, id=log_id, user=request.user)

    if request.method == 'POST':
        form = ActivityLogForm(request.POST, instance=log)
        if form.is_valid():
            activity = form.save(commit=False)

            # Recalculate CO₂
            if activity.activity_type == 'travel':
                activity.co2_emitted = activity.input_value * 0.21
            elif activity.activity_type == 'electricity':
                activity.co2_emitted = activity.input_value * 0.45
            elif activity.activity_type == 'food':
                activity.co2_emitted = activity.input_value * 1.5
            else:
                activity.co2_emitted = activity.input_value * 0.3

            activity.save()
            messages.success(request, "Activity updated successfully.")
            return redirect('dashboard')
    else:
        form = ActivityLogForm(instance=log)

    return render(request, 'tracker1/edit_activity.html', {'form': form, 'log': log})


@login_required
def leaderboard_view(request):
    # Annotate each user with total CO₂
    users = User.objects.annotate(
        total_co2=Sum('activitylog__co2_emitted')
    ).order_by('total_co2')

    return render(request, 'tracker1/leaderboard.html', {
        'users': users
    })


@login_required
def chart_view(request):
    user = request.user
    logs = ActivityLog.objects.filter(user=user)

    # Aggregate CO₂ by activity type
    data = (
        logs.values('activity_type')
        .annotate(total_co2=Sum('co2_emitted'))
        .order_by('-total_co2')
    )

    labels = [entry['activity_type'].capitalize() for entry in data]
    values = [entry['total_co2'] for entry in data]

    return render(request, 'tracker1/chart.html', {
        'labels': labels,
        'values': values
    })

from collections import Counter
from .models import ActivityLog

@login_required
def profile_view(request):
    from collections import Counter
    from datetime import datetime, timedelta
    from .models import ActivityLog, UserProfile
    from django.utils.timezone import now
    from django.db.models import Sum

    visits = request.session.get('total_visits', 0) + 1
    request.session['total_visits'] = visits

    today = datetime.now().date()
    last_visit_str = request.COOKIES.get('last_visit')
    visits_today = int(request.COOKIES.get('visits_today', 0))

    if last_visit_str:
        try:
            last_visit = datetime.strptime(last_visit_str, '%Y-%m-%d').date()
            if last_visit == today:
                visits_today += 1
            else:
                visits_today = 1
        except ValueError:
            visits_today = 1
    else:
        visits_today = 1

    logs = ActivityLog.objects.filter(user=request.user)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Get current month activity
    start_of_month = now().replace(day=1)
    co2_this_month = ActivityLog.objects.filter(
        user=request.user,
        date__gte=start_of_month
    ).aggregate(total=Sum('co2_emitted'))['total'] or 0

    # Compute progress
    goal = profile.monthly_co2_goal or 0
    progress = (co2_this_month / goal * 100) if goal > 0 else 0

    # Tips
    tips = []
    if logs.exists():
        most_common_type = Counter(logs.values_list('activity_type', flat=True)).most_common(1)[0][0]
        if most_common_type == 'travel':
            tips.append("You’ve logged a lot of travel. Try walking or biking for short distances.")
        elif most_common_type == 'electricity':
            tips.append("High electricity use? Consider switching to energy-efficient appliances.")
        elif most_common_type == 'food':
            tips.append("Eating more sustainably can lower your footprint. Try reducing meat intake.")
        elif most_common_type == 'other':
            tips.append("Try identifying which custom activities contribute most and reduce them.")
        high_input = logs.order_by('-input_value').first()
        if high_input and high_input.input_value > 50:
            tips.append(f"You logged a large input value ({high_input.input_value}). Consider moderation!")

    context = {
        'visits': visits,
        'visits_today': visits_today,
        'tips': tips,
        'profile': profile,
        'co2_saved_kg': round(co2_this_month, 2),
        'progress_percent': round(progress, 2),
    }

    response = render(request, 'tracker1/profile.html', context)
    expires = datetime.combine(today + timedelta(days=1), datetime.min.time())
    response.set_cookie('last_visit', today.strftime('%Y-%m-%d'), expires=expires)
    response.set_cookie('visits_today', visits_today, expires=expires)

    return response







@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return redirect('my_uploads')
    else:
        form = UploadForm()
    return render(request, 'tracker1/upload_file.html', {'form': form})

@login_required
def my_uploads(request):
    uploads = UploadRecord.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'tracker1/my_uploads.html', {'uploads': uploads})


@login_required
@login_required
def log_activity(request):
    if request.method == 'POST':
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user

            # Auto-calculate CO₂
            if activity.activity_type == 'travel':
                activity.co2_emitted = activity.input_value * 0.21  # 0.21 kg CO2/km for car
            elif activity.activity_type == 'electricity':
                activity.co2_emitted = activity.input_value * 0.45  # 0.45 kg CO2/kWh
            elif activity.activity_type == 'food':
                activity.co2_emitted = activity.input_value * 1.5   # 1.5 kg CO2 per meal
            else:
                activity.co2_emitted = activity.input_value * 0.3   # fallback

            activity.save()
            return redirect('dashboard')
    else:
        form = ActivityLogForm()
    return render(request, 'tracker1/log_activity.html', {'form': form})


@login_required
def dashboard(request):
    logs = ActivityLog.objects.filter(user=request.user).order_by('-date')

    # Get query parameters
    query = request.GET.get('q', '')
    activity_type = request.GET.get('type', '')

    # Apply filters
    if query:
        logs = logs.filter(description__icontains=query)
    if activity_type:
        logs = logs.filter(activity_type=activity_type)

    total = sum(log.co2_emitted for log in logs)

    return render(request, 'tracker1/dashboard.html', {
        'logs': logs,
        'total': total,
        'query': query,
        'selected_type': activity_type
    })



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, "Registration successful.")
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'tracker1/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

def about_view(request):
    return render(request, 'tracker1/about.html')

def contact_view(request):
    return render(request, 'tracker1/contact.html')

def team_view(request):
    return render(request, 'tracker1/team.html')

@login_required
def view_my_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'tracker1/view_my_profile.html', {
        'user': request.user,
        'profile': profile,
        'form': form
    })


@login_required
def set_goal(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        goal = float(request.POST.get('monthly_goal', 0))
        profile.monthly_co2_goal = goal
        profile.save()
    return redirect('profile')


