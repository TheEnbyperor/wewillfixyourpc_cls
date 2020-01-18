import json
import urllib.parse

import django_keycloak_auth.users
import django_keycloak_auth.clients
import phonenumbers
import requests
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from . import forms, models, print_label


@login_required
@permission_required('tickets.view_ticket', raise_exception=True)
def view_tickets(request):
    if request.method == "POST" and request.user.has_perm('tickets.change_ticket'):
        selected_tickets = list(
            map(
                lambda k: get_object_or_404(models.Ticket, id=k[len("select-ticket-"):]),
                filter(
                    lambda k: k.startswith("select-ticket-"),
                    request.POST.keys()
                )
            )
        )
        if request.POST.get("set") is not None:
            status = get_object_or_404(models.Status, name=request.POST.get("set"))
            for ticket in selected_tickets:
                ticket.status = status
                ticket.save()

    today_tickets = models.Ticket.objects.filter(to_do_by__gte=timezone.now().date()).order_by('-id')
    not_today_tickets = models.Ticket.objects.filter(Q(to_do_by__lt=timezone.now().date()) | Q(to_do_by__isnull=True)).order_by('-id')
    rebuild_tickets = not_today_tickets.filter(location__name="Rebuild")
    awaiting_customer_decision_tickets = not_today_tickets.filter(location__name="Awaiting Customer Decision")
    awaiting_parts_tickets = not_today_tickets.filter(location__name="Awaiting Parts")
    looking_for_parts_tickets = not_today_tickets.filter(location__name="Looking for Parts")
    completed_tickets = not_today_tickets.filter(location__name="Completed")
    normal_tickets = not_today_tickets.filter(
        ~Q(location__name="Rebuild"), ~Q(location__name="Awaiting Customer Decision"),
        ~Q(location__name="Awaiting Parts"), ~Q(location__name="Looking for Parts"),
        ~Q(location__name="Completed"),
    )

    client = django_keycloak_auth.clients.get_keycloak_admin_client()
    client_id = next(
            filter(
                lambda c: c.get("clientId") == settings.OIDC_CLIENT_ID,
                client.clients.all()
            )
    )

    agents = list(
        map(
            lambda u: {
                "user": u,
                "count": models.Ticket.objects.filter(Q(assigned_to=u.get('id')), ~Q(location__name="Completed")).count() +
                         models.Job.objects.filter(assigned_to=u.get('id'), completed=False).count()
            },
            client._client.get(
                url=client._client.get_full_url(
                    'auth/admin/realms/{realm}/clients/{id}/roles/{role_name}/users'
                        .format(realm=client._name, id=client_id.get("id"), role_name="agent")
                )
            )
        )
    )

    return render(request, 'tickets/tickets.html', {
        "today_tickets": today_tickets,
        "normal_tickets": normal_tickets,
        "rebuild_tickets": rebuild_tickets,
        "awaiting_customer_decision_tickets": awaiting_customer_decision_tickets,
        "awaiting_parts_tickets": awaiting_parts_tickets,
        "looking_for_parts_tickets": looking_for_parts_tickets,
        "completed_tickets": completed_tickets,
        "agents": agents
    })


@login_required
@permission_required('tickets.add_ticket', raise_exception=True)
def new_ticket(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        if customer_id:
            return redirect("tickets:new_step2", customer_id)
        response = redirect("customers:new")
        response["Location"] += "?" + urllib.parse.urlencode({
            "customer_name": request.POST.get("name"),
            "next": request.get_full_path()
        })
        return response
    else:
        if request.GET.get("customer_id"):
            return redirect("tickets:new_step2", request.GET["customer_id"])

    return render(request, "tickets/new_ticket.html")


@login_required
@permission_required('customers.view_customer', raise_exception=True)
def search_customer(request):
    if not request.method == "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    query = request.POST.get("name").lower().strip().split(" ")
    customers = list(
        filter(
            lambda u: any((q in u.get("firstName", "").lower().strip() or q in u.get("lastName", "").lower().strip() or
                           q in u.get("email", "").lower().strip()) for q in query),
            map(
                lambda u: u.user,
                django_keycloak_auth.users.get_users()
            )
        )
    )
    return HttpResponse(json.dumps(customers))


@login_required
@permission_required('tickets.add_ticket', raise_exception=True)
def new_ticket_step2(request, customer_id):
    ticket = models.Ticket(customer=customer_id)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, instance=ticket)
        form.clead()
        if form.is_valid():
            form.save()

            num = 1 + form.cleaned_data["additional_labels"]
            if form.cleaned_data["has_charger"]:
                num += 1
            if form.cleaned_data["has_case"]:
                num += 1
            print_label.print_ticket_label(form.instance, num=num)

            models.TicketRevision(
                ticket=form.instance,
                user=form.cleaned_data['updater'],
                data=json.dumps({
                    "type": "create"
                })
            ).save()

            return redirect("tickets:view_tickets")
    else:
        form = forms.TicketForm(instance=ticket)

    return render(request, "tickets/ticket_form.html", {
        "form": form,
        "title": "New ticket"
    })


@login_required
@permission_required('tickets.change_ticket', raise_exception=True)
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, instance=ticket)
        form.clean()
        if form.is_valid():
            for e in form.changed_data:
                if e not in ['updater', 'additional_labels']:
                    models.TicketRevision(
                        ticket=form.instance,
                        user=form.cleaned_data['updater'],
                        data=json.dumps({
                            "type": "update",
                            "field_name": form.fields[e].label,
                            "old_value": getattr(form.instance, e),
                            "new_value": form.cleaned_data[e]
                        })
                    ).save()
            form.save()

            num = form.cleaned_data["additional_labels"]
            if num:
                print_label.print_ticket_label(ticket, num=num)

            return redirect("tickets:view_tickets")
    else:
        form = forms.TicketForm(instance=ticket)

    return render(request, "tickets/ticket_form.html", {
        "form": form,
        "title": "Edit ticket"
    })


@login_required
@permission_required('tickets.view_ticket', raise_exception=True)
def print_ticket_label(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    print_label.print_ticket_label(ticket)

    return redirect(request.META.get("HTTP_REFERER"))


@login_required
@permission_required('tickets.view_ticket', raise_exception=True)
def print_ticket_receipt(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    print_label.print_ticket_receipt(ticket)

    return redirect(request.META.get("HTTP_REFERER"))


@login_required
@permission_required('tickets.change_ticket', raise_exception=True)
def send_ticket_update(request):
    if request.method == "POST":
        if not request.POST.get("ticket_id"):
            raise Http404()
        ticket = get_object_or_404(models.Ticket, id=request.POST.get("ticket_id"))
        update_type = request.POST.get("update_type")
        if update_type == "ready":
            context = {
                "content": "Your repair is complete and your device is ready to collect at your earliest convenience",
                "ticket": ticket
            }
            html_email = render_to_string("emails/ticket_update.html", context)
            plain_email = render_to_string("emails/ticket_update_plain.html", context)
            text_message = f"Your We Will Fix Your PC repair (ticket #{ticket.id}) of a {ticket.equipment.name} is " \
                f"complete and your device is ready to collect at your earliest convenience"
        elif update_type == "custom":
            context = {
                "content": request.POST.get("update_text"),
                "ticket": ticket
            }
            html_email = render_to_string("emails/ticket_update.html", context)
            plain_email = render_to_string("emails/ticket_update_plain.html", context)
            text_message = f"An update on your We Will Fix Your PC (ticket #{ticket.id}) repair of a " \
                f"{ticket.equipment.name} :\n {request.POST.get('update_text')}"
        else:
            return HttpResponseBadRequest()

        customer = ticket.get_customer()

        if customer.get("email"):
            mail = EmailMultiAlternatives(
                'An update on your We Will Fix Your PC repair', plain_email,
                'noreply@noreply.wewillfixyourpc.co.uk', [customer.get("email")]
            )
            mail.attach_alternative(html_email, 'text/html')
            mail.send()

        mobile_numbers = []
        other_numbers = []
        for n in customer.get("attributes", {}).get("phone", []):
            try:
                n = phonenumbers.parse(n, settings.PHONENUMBER_DEFAULT_REGION)
            except phonenumbers.phonenumberutil.NumberParseException:
                continue
            if phonenumbers.is_valid_number(n):
                if phonenumbers.phonenumberutil.number_type(n) == phonenumbers.PhoneNumberType.MOBILE:
                    mobile_numbers.append(n)
                else:
                    other_numbers.append(n)

        if len(mobile_numbers):
            for n in mobile_numbers:
                r = requests.post("https://rest.nexmo.com/sms/json", data={
                    "from": "We Will Fix",
                    "to": phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)[1:],
                    "text": text_message,
                    "api_key": settings.NEXMO_KEY,
                    "api_secret": settings.NEXMO_SECRET
                })
                print(r.text)
        else:
            for n in other_numbers:
                requests.post("https://rest.nexmo.com/sms/json", data={
                    "from": "We Will Fix",
                    "to": phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)[1:],
                    "text": text_message,
                    "api_key": settings.NEXMO_KEY,
                    "api_secret": settings.NEXMO_SECRET
                })

    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if not (request.user.has_perm("tickets.view_tickets") or str(ticket.customer) == request.user.username):
        raise PermissionError()

    return render(request, "tickets/ticket.html", {
        "ticket": ticket
    })


@login_required
@permission_required('tickets.change_equipmenttype', raise_exception=True)
@permission_required('tickets.add_equipmenttype', raise_exception=True)
@permission_required('tickets.delete_equipmenttype', raise_exception=True)
@permission_required('tickets.view_equipmenttype', raise_exception=True)
@permission_required('tickets.change_ostype', raise_exception=True)
@permission_required('tickets.add_ostype', raise_exception=True)
@permission_required('tickets.delete_ostype', raise_exception=True)
@permission_required('tickets.view_ostype', raise_exception=True)
@permission_required('tickets.change_location', raise_exception=True)
@permission_required('tickets.add_location', raise_exception=True)
@permission_required('tickets.delete_location', raise_exception=True)
@permission_required('tickets.view_location', raise_exception=True)
@permission_required('tickets.change_status', raise_exception=True)
@permission_required('tickets.add_status', raise_exception=True)
@permission_required('tickets.delete_status', raise_exception=True)
@permission_required('tickets.view_status', raise_exception=True)
def ticket_settings(request):
    if request.method == 'POST':
        equipment_types = forms.EquipmentTypeFormSet(request.POST, prefix='equipment_type')
        statuses = forms.StatusFormSet(request.POST, prefix='status')
        locations = forms.LocationFormSet(request.POST, prefix='location')
        os_types = forms.OSTypeFormSet(request.POST, prefix='os_type')
        equipment_types.clean()
        statuses.clean()
        locations.clean()
        os_types.clean()
        if equipment_types.is_valid() and statuses.is_valid() and locations.is_valid() and os_types.is_valid():
            equipment_types.save()
            statuses.save()
            locations.save()
            os_types.save()

            equipment_types = forms.EquipmentTypeFormSet(prefix='equipment_type')
            statuses = forms.StatusFormSet(prefix='status')
            locations = forms.LocationFormSet(prefix='location')
            os_types = forms.OSTypeFormSet(prefix='os_type')
    else:
        equipment_types = forms.EquipmentTypeFormSet(prefix='equipment_type')
        statuses = forms.StatusFormSet(prefix='status')
        locations = forms.LocationFormSet(prefix='location')
        os_types = forms.OSTypeFormSet(prefix='os_type')

    return render(request, 'tickets/settings.html', {
        "equipment_types": equipment_types,
        "statuses": statuses,
        "locations": locations,
        "os_types": os_types,
    })


@login_required
@permission_required('tickets.add_job', raise_exception=True)
def new_job(request):
    if request.method == 'POST':
        form = forms.JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tickets:view_tickets")
    else:
        form = forms.JobForm()

    return render(request, "tickets/job_form.html", {
        "form": form,
        "title": "New job"
    })


@login_required
@permission_required('tickets.change_job', raise_exception=True)
def edit_job(request, job_id):
    job = get_object_or_404(models.Job, id=job_id)
    if request.method == 'POST':
        form = forms.JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("tickets:view_tickets")
    else:
        form = forms.JobForm(instance=job)

    return render(request, "tickets/job_form.html", {
        "form": form,
        "title": "Edit job"
    })


@login_required
@permission_required('tickets.view_job', raise_exception=True)
def view_job(request, job_id):
    job = get_object_or_404(models.Job, id=job_id)
    return render(request, "tickets/job.html", {
        "job": job
    })


@login_required
@permission_required('tickets.view_job', raise_exception=True)
def view_jobs(request, user_id):
    jobs = models.Job.objects.filter(assigned_to=user_id)
    tickets = models.Ticket.objects.filter(assigned_to=user_id)
    user = models.get_user(user_id)
    return render(request, "tickets/jobs.html", {
        "jobs": jobs,
        "tickets": tickets,
        "user": user
    })