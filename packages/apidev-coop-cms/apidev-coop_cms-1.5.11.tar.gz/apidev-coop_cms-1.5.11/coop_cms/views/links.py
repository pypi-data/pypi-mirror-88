# -*- coding: utf-8 -*-
"""links: object who redirects to another url"""

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.api import success as success_message
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from colorbox.decorators import popup_redirect

from coop_cms.forms.content import NewLinkForm
from coop_cms import models
from coop_cms.moves import reverse


@login_required(login_url=reverse_lazy('login'))
@popup_redirect
def new_link(request):
    """new link"""
    content_type = ContentType.objects.get_for_model(models.Link)
    perm = '{0}.add_{1}'.format(content_type.app_label, content_type.model)

    if not request.user.has_perm(perm):
        raise PermissionDenied

    if request.method == "POST":
        form = NewLinkForm(request.POST)
        if form.is_valid():
            form.save()
            form.save_m2m()
            homepage_url = reverse('coop_cms_homepage')
            next_url = request.META.get('HTTP_REFERER', homepage_url)
            success_message(request, _('The link has been created properly'))
            return HttpResponseRedirect(next_url)
    else:
        form = NewLinkForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'coop_cms/popup_new_link.html',
        context
    )
