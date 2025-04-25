from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from .models import IPOListing, IPOApplication, UserProfile
from django.db.models import Count, Sum
from datetime import timedelta

# Create your views here.

@staff_member_required
def admin_dashboard(request):
    # Get current date
    today = timezone.now().date()
    
    # IPO Statistics
    total_ipos = IPOListing.objects.count()
    upcoming_ipos = IPOListing.objects.filter(status='upcoming').count()
    open_ipos = IPOListing.objects.filter(status='open').count()
    closed_ipos = IPOListing.objects.filter(status='closed').count()
    
    # Application Statistics
    total_applications = IPOApplication.objects.count()
    pending_applications = IPOApplication.objects.filter(status='pending').count()
    approved_applications = IPOApplication.objects.filter(status='approved').count()
    rejected_applications = IPOApplication.objects.filter(status='rejected').count()
    
    # Recent Applications
    recent_applications = IPOApplication.objects.select_related('user', 'ipo').order_by('-application_date')[:10]
    
    # User Statistics
    total_users = UserProfile.objects.count()
    verified_users = UserProfile.objects.filter(is_verified=True).count()
    unverified_users = total_users - verified_users
    
    # Upcoming IPOs
    upcoming_ipos_list = IPOListing.objects.filter(
        status='upcoming',
        subscription_start__gte=today
    ).order_by('subscription_start')[:5]
    
    # Recent Activity
    recent_activity = IPOApplication.objects.select_related('user', 'ipo').order_by('-updated_at')[:10]
    
    context = {
        'total_ipos': total_ipos,
        'upcoming_ipos': upcoming_ipos,
        'open_ipos': open_ipos,
        'closed_ipos': closed_ipos,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'recent_applications': recent_applications,
        'total_users': total_users,
        'verified_users': verified_users,
        'unverified_users': unverified_users,
        'upcoming_ipos_list': upcoming_ipos_list,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'admin/dashboard.html', context)
