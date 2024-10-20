from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, BadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django import forms


from .models import Party, Election, Statement, StatementAnswer
from .forms import StatementAnswerForm

# Create your views here.
@login_required
def party(request, election_slug=None):
    # Vstopna stran do vprašalnika za stranke.
    # Če uporabnik ni vpisan, ga preusmeri na login.
    # Če je vpisan, pa ni party, onemogoči dostop.
    # Če stranka še ni zaključila vprašalnika, jo preusmeri na navodila.
    # Če je stranka že zaključila vprašalnik, jo preusmeri na povzetek.

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    if party.finished_quiz:
        return redirect(f"/{election.slug}/stranke/povzetek")
    else:
        return redirect(f"/{election.slug}/stranke/navodila")


@login_required
def party_instructions(request, election_slug=None):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    if party.finished_quiz:
        return redirect(f"/{election_slug}/stranke/povzetek")

    # categories = WorkGroup.objects.filter(election=election).order_by("id")

    # for cat in categories:
    #     demands = Demand.objects.filter(workgroup=cat, election=election)
    #     if party.municipality:
    #         demands = demands.filter(municipality=party.municipality)
    #     cat.check = len(
    #         DemandAnswer.objects.filter(
    #             party=party, agree_with_demand__isnull=False, demand__workgroup=cat
    #         )
    #     ) == len(demands)

    # next = WorkGroup.objects.filter(election=election).order_by("id").first().id

    return render(
        request,
        "navodila.html",
        context={
            # "statements": statements,
            "step": 1,
            "election_slug": election_slug,
            # "next": next,
        },
    )


@login_required
def party_finish(request, election_slug=None):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    if party.finished_quiz:
        return redirect(f"/{election.slug}/stranke/povzetek")

    # categories = WorkGroup.objects.filter(election=election).order_by("id")
    # for cat in categories:
    #     demands = Demand.objects.filter(workgroup=cat, election=election)
    #     if party.municipality:
    #         demands = demands.filter(municipality=party.municipality)
    #     cat.check = len(
    #         DemandAnswer.objects.filter(
    #             party=party, agree_with_demand__isnull=False, demand__workgroup=cat
    #         )
    #     ) == len(demands)

    statements = Statement.objects.filter(election=election)

    allow_submit = len(
        StatementAnswer.objects.filter(party=party, answer__isnull=False)
    ) == len(statements)
    finished_quiz = party.finished_quiz

    return render(
        request,
        "zakljucek.html",
        context={
            "step": 3,
            "allow_submit": allow_submit,
            "finished_quiz": finished_quiz,
            "election_slug": election_slug,
        },
    )


@login_required
def party_save(request, election_slug=None):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    party.finished_quiz = True
    party.save()

    return redirect(f"/{election.slug}/stranke/povzetek")


@login_required
def party_summary(request, election_slug=None):

    # if user is not a party, restrict access
    try:
        party = Party.objects.get(user=request.user)
    except:
        raise PermissionDenied
    # ---------------------------------------

    if election_slug is None:
        election = Election.objects.first()
    else:
        election = Election.objects.get(slug=election_slug)

    party = Party.objects.get(user=request.user)

    answers = StatementAnswer.objects.filter(party=party)

    return render(
        request,
        "povzetek.html",
        context={
            "answers": answers,
            "election_slug": election_slug,
        },
    )


class PartyDemand(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, election_slug=None):
        # if user is not a party, restrict access
        try:
            party = Party.objects.get(user=request.user)
        except:
            raise PermissionDenied
        # ---------------------------------------

        if election_slug is None:
            election = Election.objects.first()
        else:
            election = Election.objects.get(slug=election_slug)

        if party.finished_quiz:
            return redirect(f"/{election.slug}/stranke/povzetek")

        statements = Statement.objects.filter(election=election)

        # # for sidebar menu
        # categories = WorkGroup.objects.filter(election=election).order_by("id")
        # for cat in categories:
        #     demands = Demand.objects.filter(workgroup=cat)
        #     if party.municipality:
        #         demands = demands.filter(municipality=party.municipality)
        #     cat.check = len(
        #         DemandAnswer.objects.filter(
        #             party=party, agree_with_demand__isnull=False, demand__workgroup=cat
        #         )
        #     ) == len(demands)

        # # TODO: treba prilagodit za non-existend work groupe
        # category = WorkGroup.objects.get(pk=category_id)
        # demands = Demand.objects.filter(workgroup=category).order_by("id")
        # if party.municipality:
        #     demands = demands.filter(municipality=party.municipality)

        StatementAnswersFormSet = forms.formset_factory(
            StatementAnswerForm, extra=len(statements)
        )
        statements_formset = StatementAnswersFormSet()

        f = []

        for statement in statements:
            da_form = {
                "statement": statement.pk,
                "party": party.pk,
                "answer": None,
                "comment": "",
                "title": statement.title,
                # "description": statement.description,
                # "priority_demand": demand.priority_demand,
            }

            try:
                statement_answer = StatementAnswer.objects.get(
                    statement=statement.pk, party=party.pk
                )
                da_form["answer"] = statement_answer.answer
                da_form["comment"] = statement_answer.comment
                # print("da form comment", da_form["comment"])

            except:
                pass

            finally:
                f.append(da_form)

        return render(
            request,
            "stranke.html",
            context={
                "forms": f,
                "formset": statements_formset,
                "election_slug": election_slug,
                "step": 2,
            },
        )

    def post(self, request, election_slug=None):

        # if user is not a party, restrict access
        try:
            party = Party.objects.get(user=request.user)
        except:
            raise PermissionDenied
        # ---------------------------------------

        if election_slug is None:
            election = Election.objects.first()
        else:
            election = Election.objects.get(slug=election_slug)

        if party.finished_quiz:
            raise BadRequest

        StatementAnswersFormSet = forms.formset_factory(StatementAnswerForm)
        formset = StatementAnswersFormSet(request.POST or None)

        for form in formset:
            if form.is_valid():
                form.save()
            else:
                da = StatementAnswer.objects.get(
                    statement=form["statement"].value(), party=party.pk
                )
                da.answer = form["answer"].value()
                da.comment = form["comment"].value()
                da.save()

        return redirect(f"/{election.slug}/stranke/oddaja")
