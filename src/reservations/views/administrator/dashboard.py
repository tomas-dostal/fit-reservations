from django.shortcuts import render
from django.views.generic import View

from reservations.decorators import user_passes_test


class AdminDashboard(View):
    @user_passes_test(
        lambda u: u.is_superuser
        or u.has_perm("reservations.is_group_manager")
        or u.has_perm("reservations.is_room_manager")
    )
    def get_dashboard(request):
        return render(request, "administrator/dashboard/main.html", {})
