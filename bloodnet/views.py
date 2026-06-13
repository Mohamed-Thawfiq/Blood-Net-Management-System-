from django.shortcuts import render, redirect
from .models import *
from .form import *
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import date


class adding_donor(LoginRequiredMixin,View):
    login_url = '/'
    def get(self, request):
        context = {
            'donor_form': donor_form(),
            'page_title': 'Add Donor',
            'subtitle': 'Register a new donor 🩸',
            'button_text': 'Add Donor'
        }
        return render(request, 'donor_form.html', context)

    def post(self, request):
        donor_data = donor_form(request.POST)
        if donor_data.is_valid():
            donor = donor_data.save(commit=False)
            donor.area_manager = request.user
            try:
                donor.area = Area.objects.get(name=request.user.area)
            except Exception:
                pass
            donor.save()
            return redirect('/donor/view/')
        context = {
            'donor_form': donor_data,
            'page_title': 'Add Donor',
            'subtitle': 'Register a new donor 🩸',
            'button_text': 'Add Donor'
        }
        return render(request, 'donor_form.html', context)


class donor_view(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        context = {
            'all_donor': add_donors.objects.filter(area_manager=request.user)
        }
        return render(request, 'view_donor.html', context)


class donor_delete(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, id):
        donor = add_donors.objects.filter(id=id, area_manager=request.user).first()
        if donor:
            donor.delete()
        return redirect('/donor/view/')


class donor_update(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, id):
        updated_donor = add_donors.objects.get(id=id)
        context = {
            'donor_form': donor_form(instance=updated_donor),
            'page_title': 'Update Donor Details',
            'subtitle': 'Ensure donor information remains accurate 🩸',
            'button_text': 'Update Donor'
        }
        return render(request, 'donor_form.html', context)

    def post(self, request, id):
        updated_donor = add_donors.objects.get(id=id)
        donors_form = donor_form(request.POST, instance=updated_donor)
        if donors_form.is_valid():
            donors_form.save()
            return redirect('/donor/view/')
        context = {
            'donor_form': donors_form,
            'page_title': 'Update Donor Details',
            'subtitle': 'Ensure donor information remains accurate 🩸',
            'button_text': 'Update Donor'
        }
        return render(request, 'donor_form.html', context)


class blood_requests(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        from authentication.models import User
        context = {
            'managers': User.objects.filter(role=1, is_approved=True),
            'area_managers': User.objects.filter(
                role=2, is_approved=True
            ).exclude(id=request.user.id),
        }
        return render(request, 'blood_form.html', context)

    def post(self, request):
        from authentication.models import User
        patient_name = request.POST.get('patient_name')
        patient_age = request.POST.get('patient_age')
        patient_contact = request.POST.get('patient_contact')
        patient_bg = request.POST.get('patient_bg')
        hospital_name = request.POST.get('hospital_name')
        hospital_area = request.POST.get('hospital_area')
        blood_units = request.POST.get('blood_units', 1)
        last_date = request.POST.get('last_date')
        recipient_id = request.POST.get('recipient_id')
        recipient_type = request.POST.get('recipient_type')

        assigned_am = None
        area_obj = None

        try:
            if recipient_type == 'area_manager' and recipient_id:
                assigned_am = User.objects.get(id=recipient_id, role=2)
                area_obj = Area.objects.filter(
                    area_manager=assigned_am
                ).first()
            elif recipient_type == 'manager' and recipient_id:
                assigned_am = User.objects.get(id=recipient_id, role=1)
        except Exception:
            pass

        blood_request.objects.create(
            patient_name=patient_name,
            patient_age=int(patient_age) if patient_age else 0,
            patient_contact=patient_contact or '',
            patient_bg=patient_bg or '',
            hospital_name=hospital_name or '',
            hospital_area=hospital_area or '',
            blood_units=int(blood_units),
            last_date=last_date or None,
            requested_by=request.user,
            area=area_obj,
            assigned_area_manager=assigned_am,
        )
        return redirect('/donor/bloodreq/')

class viewreq(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        context = {
            'all_request': blood_request.objects.filter(
                assigned_area_manager=request.user
            )
        }
        return render(request, 'blood_req.html', context)


class request_action(LoginRequiredMixin, View):
    login_url = '/'
    def post(self, request, id):
        req = blood_request.objects.get(id=id)
        action = request.POST.get('action')
        units_completed = request.POST.get('units_completed', req.blood_units)

        donation_history.objects.create(
            request=req,
            action=action,
            patient_name=req.patient_name,
            patient_age=req.patient_age,
            patient_contact=req.patient_contact,
            patient_bg=req.patient_bg,
            hospital_name=req.hospital_name,
            blood_units=int(units_completed) if action == 'donated' else 0,
            area_manager=request.user,
        )
        req.delete()
        return redirect('/donor/bloodreq/')


class donation_history_view(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        context = {
            'history': donation_history.objects.filter(
                area_manager=request.user
            ).order_by('-processed_at'),
            'donation_count': donation_history.objects.filter(
                area_manager=request.user, action='donated'
            ).count(),
            'dropped_count': donation_history.objects.filter(
                area_manager=request.user, action='dropped'
            ).count(),
            'completed_units': donation_history.objects.filter(
                area_manager=request.user, action='donated'
            ).aggregate(total=Sum('blood_units'))['total'] or 0,
        }
        return render(request, 'history.html', context)


class appoint_donor(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        temp_rejected_ids = list(temporary_rejection.objects.filter(
            available_date__gt=date.today(),
            donor__area_manager=request.user
        ).values_list('donor_id', flat=True))
        perm_rejected_ids = list(permanent_rejection.objects.filter(
            donor__area_manager=request.user
        ).values_list('donor_id', flat=True))
        appointed_ids = list(donor_appointment.objects.filter(
            donor__area_manager=request.user
        ).values_list('donor_id', flat=True))
        excluded_ids = temp_rejected_ids + perm_rejected_ids + appointed_ids
        all_donors = add_donors.objects.filter(
            area_manager=request.user
        ).exclude(id__in=excluded_ids)
        return render(request, 'appoint_donor.html', {'all_donors': all_donors})


class call_appointment_process(LoginRequiredMixin, View):
    login_url = '/'
    def post(self, request, id):
        donor = add_donors.objects.get(id=id)
        action = request.POST.get('action')
        patient_name = request.POST.get('patient_name', '')
        appointment_date = request.POST.get('appointment_date', '')
        reason = request.POST.get('reason', '')
        available_date = request.POST.get('available_date', '')

        if action == 'appointed':
            donor_appointment.objects.create(
                donor=donor,
                patient_name=patient_name,
                appointment_date=appointment_date
            )
        elif action == 'temp_reject':
            temporary_rejection.objects.create(
                donor=donor,
                reason=reason,
                available_date=available_date
            )
        elif action == 'perm_reject':
            permanent_rejection.objects.create(
                donor=donor,
                reason=reason
            )
        return redirect('/donor/appoint/')


class temporary_rejection_view(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        temp_rejections = temporary_rejection.objects.filter(
            available_date__gt=date.today(),
            donor__area_manager=request.user
        )
        context = {'temp_rejections': temp_rejections}
        return render(request, 'temporary_rejection.html', context)


class permanent_rejection_view(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, id=None):
        perm_rejections = permanent_rejection.objects.filter(
            donor__area_manager=request.user
        )
        context = {'perm_rejections': perm_rejections}
        return render(request, 'permanent_rejection.html', context)

    def post(self, request, id=None):
        if id:
            try:
                perm_obj = permanent_rejection.objects.get(id=id)
                donor = perm_obj.donor  # get the actual donor
                perm_obj.delete()       # delete rejection record
                donor.delete()          # delete donor from add_donors too
            except permanent_rejection.DoesNotExist:
                pass
        return redirect('/donor/permanent-rejection/')


class appointed_donor_view(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        context = {
            'appointments': donor_appointment.objects.filter(
                donor__area_manager=request.user
            ).order_by('-created_at')
        }
        return render(request, 'appointed_donors.html', context)


class appointment_action(LoginRequiredMixin, View):
    login_url = '/'
    def post(self, request, id):
        appointment = donor_appointment.objects.get(id=id)
        action = request.POST.get('action')

        if action == 'donated':
            available_date = timezone.now().date() + relativedelta(months=3)
            temporary_rejection.objects.create(
                donor=appointment.donor,
                reason='Donated blood - 3 month recovery period',
                available_date=available_date
            )
            appointment.delete()

        elif action == 'not_donated':
            appointment.delete()

        return redirect('/donor/appointed/')