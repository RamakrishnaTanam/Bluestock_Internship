from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import IPOListing, IPOApplication

@staff_member_required
def ipo_dashboard(request):
    # Get IPO statistics
    total_ipos = IPOListing.objects.count()
    upcoming_ipos = IPOListing.objects.filter(status='upcoming').count()
    open_ipos = IPOListing.objects.filter(status='open').count()
    closed_ipos = IPOListing.objects.filter(status='closed').count()
    
    # Get application statistics
    total_applications = IPOApplication.objects.count()
    pending_applications = IPOApplication.objects.filter(status='pending').count()
    approved_applications = IPOApplication.objects.filter(status='approved').count()
    rejected_applications = IPOApplication.objects.filter(status='rejected').count()
    
    # Get recent applications
    recent_applications = IPOApplication.objects.select_related('user', 'ipo').order_by('-application_date')[:10]
    
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
    }
    
    return render(request, 'ipo/dashboard.html', context) 