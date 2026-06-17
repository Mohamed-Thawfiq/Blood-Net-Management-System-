from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import User
from bloodnet.models import Area


class loginpage(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.role == 1:
                return redirect('/dashboard/manager/')
            if request.user.role == 2:
                return redirect('/donor/view/')
        return render(request, 'login.html')

    def post(self, request):
        id_num = request.POST.get('id_num', '').strip()
        password = request.POST.get('password', '')

        try:
            user_obj = User.objects.get(id_num=id_num)
            if user_obj.check_password(password):
                if not user_obj.is_approved:
                    return render(request, 'login.html', {
                        'error': 'Your account is pending manager approval.'
                    })
                login(request, user_obj)
                return self._redirect_by_role(user_obj)
            else:
                error = 'Invalid Membership ID or password.'
        except User.DoesNotExist:
            error = 'Invalid Membership ID or password.'

        return render(request, 'login.html', {
            'error': error,
            'form_data': {'id_num': id_num}
        })

    def _redirect_by_role(self, user):
        if user.role == 1:
            return redirect('/dashboard/manager/')
        return redirect('/dashboard/area/')


class logoutuser(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class registerpage(View):
    def get(self, request):
        available_areas = Area.objects.filter(area_manager__isnull=True)
        return render(request, 'register.html', {
            'available_areas': available_areas
        })

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        contact = request.POST.get('contact', '').strip()
        id_num = request.POST.get('id_num', '').strip()
        area_id = request.POST.get('area_id', '').strip()
        available_areas = Area.objects.filter(area_manager__isnull=True)

        error = None
        area_obj = None

        if not all([username, password, confirm_password, contact, id_num, area_id]):
            error = 'All fields are required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif User.objects.filter(id_num=id_num).exists():
            error = 'Membership ID already registered. Use a different ID.'
        else:
            try:
                area_obj = Area.objects.get(id=area_id, area_manager__isnull=True)
            except Area.DoesNotExist:
                error = 'Selected area is not available.'

        if error or area_obj is None:
            return render(request, 'register.html', {
                'error': error or 'Selected area is not available.',
                'available_areas': available_areas,
                'form_data': request.POST
            })

        user = User(
            username=f"{username}_{area_obj.name}",  # makes it unique
            contact=contact,
            id_num=id_num,
            area=area_obj.name,
            role=2,
            is_approved=False
            )
        user.set_password(password)
        user.save()

        return render(request, 'register.html', {
            'success': 'Registration submitted! Wait for manager approval before logging in.',
            'available_areas': Area.objects.filter(area_manager__isnull=True)
        })

class ManagerDashboard(View):
    def get(self, request):
        if not request.user.is_authenticated or request.user.role != 1:
            return redirect('/')
        from bloodnet.models import (
            add_donors, blood_request,
            donation_history, TerminatedAreaManagerBackup
        )
        from django.db.models import Sum, Count

        areas = Area.objects.all()
        pending_ams = User.objects.filter(role=2, is_approved=False)
        active_ams = User.objects.filter(role=2, is_approved=True)
        backups = TerminatedAreaManagerBackup.objects.all().order_by('-terminated_at')

        # Analytics per area manager
        am_stats = []
        for am in active_ams:
            donated = donation_history.objects.filter(
                area_manager=am, action='donated'
            ).count()
            dropped = donation_history.objects.filter(
                area_manager=am, action='dropped'
            ).count()
            units = donation_history.objects.filter(
                area_manager=am, action='donated'
            ).aggregate(t=Sum('blood_units'))['t'] or 0
            donor_count = add_donors.objects.filter(area_manager=am).count()
            am_stats.append({
                'am': am,
                'donated': donated,
                'dropped': dropped,
                'units': units,
                'donors': donor_count,
            })

        # All donors grouped by area
        donors_by_area = {}
        for area in areas:
            donors_by_area[area.name] = add_donors.objects.filter(area=area)

        context = {
            'areas': areas,
            'pending_ams': pending_ams,
            'active_ams': active_ams,
            'am_stats': am_stats,
            'donors_by_area': donors_by_area,
            'backups': backups,
            'blood_requests': blood_request.objects.all().order_by('-created_at'),
        }
        return render(request, 'manager_dashboard.html', context)

    def post(self, request):
        if not request.user.is_authenticated or request.user.role != 1:
            return redirect('/')

        action = request.POST.get('action')

        # Create area
        if action == 'create_area':
            name = request.POST.get('area_name', '').strip()
            if name:
                Area.objects.get_or_create(name=name)

        # Approve area manager
        elif action == 'approve_am':
            am_id = request.POST.get('am_id')
            area_id = request.POST.get('area_id')
            try:
                am = User.objects.get(id=am_id, role=2)
                area = Area.objects.get(id=area_id)
                am.is_approved = True
                am.area = area.name
                am.save()
                area.area_manager = am
                area.save()
            except (User.DoesNotExist, Area.DoesNotExist):
                pass

        # Reject area manager
        elif action == 'reject_am':
            am_id = request.POST.get('am_id')
            try:
                User.objects.get(id=am_id, role=2).delete()
            except User.DoesNotExist:
                pass

        # Terminate area manager
        elif action == 'terminate_am':
            from bloodnet.models import add_donors, TerminatedAreaManagerBackup
            am_id = request.POST.get('am_id')
            try:
                am = User.objects.get(id=am_id, role=2)
                area = Area.objects.filter(area_manager=am).first()
                donors = add_donors.objects.filter(area_manager=am)
                donor_data = list(donors.values(
                    'donor_name', 'donor_age',
                    'donor_contact', 'blood_group'
                ))
                TerminatedAreaManagerBackup.objects.create(
                    area=area,
                    area_name=area.name if area else am.area,
                    manager_username=am.username,
                    donor_data=donor_data
                )
                if area:
                    area.area_manager = None
                    area.save()
                am.is_approved = False
                am.save()
            except User.DoesNotExist:
                pass

        # Restore backup to new area manager
        elif action == 'restore_backup':
            from bloodnet.models import add_donors, TerminatedAreaManagerBackup
            backup_id = request.POST.get('backup_id')
            am_id = request.POST.get('am_id')
            try:
                backup = TerminatedAreaManagerBackup.objects.get(id=backup_id)
                am = User.objects.get(id=am_id, role=2, is_approved=True)
                area = backup.area
                for d in backup.donor_data:
                    add_donors.objects.create(
                        donor_name=d['donor_name'],
                        donor_age=d['donor_age'],
                        donor_contact=d['donor_contact'],
                        blood_group=d['blood_group'],
                        area=area,
                        area_manager=am
                    )
                backup.delete()
            except Exception:
                pass

        # Send blood request
        elif action == 'send_request':
            from bloodnet.models import blood_request
            try:
                area = Area.objects.get(id=request.POST.get('area_id'))
                am = None
                am_id = request.POST.get('am_id')
                if am_id:
                    am = User.objects.get(id=am_id, role=2)
                blood_request.objects.create(
                    patient_name=request.POST.get('patient_name'),
                    patient_age=int(request.POST.get('patient_age', 0)),
                    patient_contact=request.POST.get('patient_contact'),
                    patient_bg=request.POST.get('patient_bg'),
                    hospital_name=request.POST.get('hospital_name'),
                    hospital_area=area.name,
                    blood_units=int(request.POST.get('blood_units', 1)),
                    last_date=request.POST.get('last_date') or None,
                    requested_by=request.user,
                    area=area,
                    assigned_area_manager=am,
                )
            except Exception:
                pass

        # Update manager profile
        elif action == 'update_profile':
            u = request.user
            new_username = request.POST.get('username', '').strip()
            new_password = request.POST.get('password', '').strip()
            new_contact = request.POST.get('contact', '').strip()
            new_id = request.POST.get('id_num', '').strip()
            if new_username:
                u.username = new_username
            if new_password:
                u.set_password(new_password)
            if new_contact:
                u.contact = new_contact
            if new_id:
                u.id_num = new_id
            u.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, u)

        return redirect('/dashboard/manager/')
    
class AreaManagerDashboard(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        if request.user.role != 2:
            return redirect('/')
        return redirect('/donor/view/')