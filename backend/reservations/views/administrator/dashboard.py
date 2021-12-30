from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views.generic import View


class AdminDashboard(View):
    @user_passes_test(
        lambda u: u.is_superuser
        or u.has_perm("reservations.is_group_manager")
        or u.has_perm("reservations.is_room_manager")
    )
    def get_dashboard(request):
        return render(request, "administrator/dashboard/main.html", {})
