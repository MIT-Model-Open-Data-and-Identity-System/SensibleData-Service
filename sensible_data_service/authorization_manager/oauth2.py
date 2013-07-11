#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from uni_form.helpers import FormHelper, Submit, Reset
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.authorize import UnvalidatedRequest, UnauthenticatedUser
from oauth2app.models import *
from oauth2app.consts import CODE, TOKEN, CODE_AND_TOKEN
from .forms import AuthorizeForm


@login_required
def missing_redirect_uri(request):
    return render_to_response(
        'oauth2/missing_redirect_uri.html',
        {},
        RequestContext(request))


@login_required
def authorize(request):
    authorizer = Authorizer(response_type=CODE_AND_TOKEN)
    try:
        authorizer.validate(request)
    except MissingRedirectURI, e:
        return HttpResponseRedirect("/authorization_manager/oauth2/missing_redirect_uri")
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    if request.method == 'GET':
        # Make sure the authorizer has validated before requesting the client
        # or access_ranges as otherwise they will be None.
        template = {
            "client":authorizer.client,
            "scopes":authorizer.access_ranges}
        template["form"] = AuthorizeForm()
        helper = FormHelper()
        no_submit = Submit('connect','No', css_class='btn btn-large')
        helper.add_input(no_submit)
        yes_submit = Submit('connect', 'Yes', css_class='btn btn-large btn-primary')
        helper.add_input(yes_submit)
        helper.form_action = '/authorization_manager/oauth2/authorize?%s' % authorizer.query_string
        helper.form_method = 'POST'
        template["helper"] = helper
        return render_to_response(
            'oauth2/authorize.html',
            template,
            RequestContext(request))
    elif request.method == 'POST':
        form = AuthorizeForm(request.POST)
        if form.is_valid():
            if request.POST.get("connect") == "Yes":
                return authorizer.grant_redirect()
            else:
                return authorizer.error_redirect()
    return HttpResponseRedirect("/")
