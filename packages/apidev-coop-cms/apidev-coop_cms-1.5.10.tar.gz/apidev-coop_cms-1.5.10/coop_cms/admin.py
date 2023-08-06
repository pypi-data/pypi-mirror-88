# -*- coding: utf-8 -*-
"""
Admin pages for coop_cms
"""

from django.conf import settings
from django.contrib import admin
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from coop_cms.forms.articles import ArticleAdminForm
from coop_cms.forms.content import AliasAdminForm
from coop_cms.forms.navigation import NavTypeForm, NavNodeAdminForm
from coop_cms.forms.newsletters import NewsletterItemAdminForm, NewsletterAdminForm
from coop_cms import models
from coop_cms.settings import get_article_class, import_module


# The BASE_ADMIN_CLASS can be a Translation admin if needed or regular modelAdmin if not
if 'modeltranslation' in settings.INSTALLED_APPS:
    BASE_ADMIN_CLASS = import_module('modeltranslation.admin').TranslationAdmin
else:
    BASE_ADMIN_CLASS = admin.ModelAdmin


def clear_thumbnails_action(model_admin, request, queryset):
    """This action is used by Image Admin and cause sorl-thumbnails to be reset"""
    for obj in queryset:
        obj.clear_thumbnails()


clear_thumbnails_action.short_description = _("Clear thumbnails")


@admin.register(models.NavNode)
class NavNodeAdmin(admin.ModelAdmin):
    """Navigation node admin"""
    list_display = ["as_text", "label", 'parent', 'ordering', 'in_navigation', 'content_type', 'object_id']
    list_filter = ['tree', 'in_navigation', 'parent']
    list_editable = ["label", 'parent', 'ordering', 'in_navigation', ]
    ordering = ["tree", "parent", "ordering"]
    form = NavNodeAdminForm


@admin.register(models.NavType)
class NavTypeAdmin(admin.ModelAdmin):
    """Navigation type admin"""
    form = NavTypeForm


@admin.register(models.NavTree)
class NavTreeAdmin(admin.ModelAdmin):
    """Navigation tree admin"""
    list_display = ['as_text', 'name', 'navtypes_list', 'get_root_nodes_count']
    list_editable = ['name']
    list_filters = ['id']

    def nodes_li(self, tree):
        """display the tree nodes for jstree"""
        root_nodes = tree.get_root_nodes()
        nodes_li = ''.join([node.as_jstree() for node in root_nodes])
        return nodes_li

    def navtypes_list(self, tree):
        """list of navigable types"""
        if tree.types.count() == 0:
            return _('All')
        else:
            return ' - '.join(['{0}'.format(x) for x in tree.types.all()])
    navtypes_list.short_description = _('navigable types')

    def change_view(self, request, object_id, extra_context=None, *args, **kwargs):
        """override the change view"""
        extra_context = extra_context or {}
        try:
            object_id = int(object_id)
        except ValueError:
            #if the object_id is not a valid number, returns 404
            raise Http404
        tree = models.get_navtree_class().objects.get(id=object_id)
        extra_context['navtree'] = tree
        extra_context['navtree_nodes'] = self.nodes_li(tree)
        return super(NavTreeAdmin, self).change_view(
            request, str(object_id), extra_context=extra_context, *args, **kwargs
        )  # pylint: disable=E1002


@admin.register(get_article_class())
class ArticleAdmin(BASE_ADMIN_CLASS):
    """Article admin"""
    form = ArticleAdminForm
    list_display = [
        'slug', 'title', 'category', 'template_name', 'publication', 'headline', 'in_newsletter', 'modified',
        'login_required', 'is_homepage'
    ]
    list_editable = ['publication', 'headline', 'in_newsletter', 'category']
    readonly_fields = ['created', 'modified', 'is_homepage']
    list_filter = [
        'publication', 'login_required', 'headline', 'in_newsletter', 'sites',
        'category', 'template'
    ]
    date_hierarchy = 'publication_date'
    fieldsets = (
        (_('General'), {'fields': ('slug', 'title', 'subtitle', 'publication', 'login_required', )}),
        (_('Settings'), {
            'fields': ('sites', 'template', 'category', 'headline', 'is_homepage', 'logo', 'in_newsletter', )
        }),
        (_('Advanced'), {'fields': ('publication_date', 'created', 'modified', )}),
        (_('Content'), {'fields': ('content', 'summary', )}),
        (_('Debug'), {'fields': ('temp_logo', )}),
    )
    filter_vertical = ('sites', )

    def get_form(self, request, obj=None, **kwargs):
        """return custom form: It adds the current user"""
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)  # pylint: disable=E1002
        form.current_user = request.user
        return form


class MediaFilterFilter(admin.SimpleListFilter):
    """filter by media_filter"""
    title = _('Media filter')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'media_filter'

    def lookups(self, request, model_admin):
        """values of the filters"""
        media_filters = models.MediaFilter.objects.all()
        return [(x.id, x.name) for x in media_filters]

    def queryset(self, request, queryset):
        """return values after taken the filter into account"""
        value = self.value()
        if value is None:
            return queryset
        return queryset.filter(filters__id=value)


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    """Image admin"""
    list_display = ['admin_image', 'name', 'file', 'size', 'ordering', 'copyright', 'alt_text', 'title']
    list_filter = [MediaFilterFilter, 'size']
    list_editable = ('ordering', 'copyright', 'alt_text', 'title')
    search_fields = ['name']
    actions = [clear_thumbnails_action]
    readonly_fields = ['admin_image']


@admin.register(models.Fragment)
class FragmentAdmin(BASE_ADMIN_CLASS):
    """Fragment admin"""
    list_display = ['name', 'position', 'type', 'filter', 'css_class']
    list_filter = ['type', 'filter', 'css_class']


@admin.register(models.ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    """Article category Admin"""
    list_display = ['name', 'slug', 'ordering', 'in_rss', 'pagination_size']
    list_editable = ['ordering', 'in_rss']
    readonly_fields = ['slug']


@admin.register(models.NewsletterItem)
class NewsletterItemAdmin(admin.ModelAdmin):
    """newsletter item Admin"""
    form = NewsletterItemAdminForm
    list_display = ['content_type', 'content_object', 'ordering']
    list_editable = ['ordering']
    fieldsets = (
        (_('Article'), {'fields': ('object_id', 'content_type', 'ordering')}),
    )


@admin.register(models.Newsletter)
class NewsletterAdmin(BASE_ADMIN_CLASS):
    """Newsletter Admin"""

    form = NewsletterAdminForm
    raw_id_fields = ['items']
    list_display = ['subject', 'template', 'source_url']

    def get_form(self, request, obj=None, **kwargs):
        """return custom form: it adds the current user"""
        form = super(NewsletterAdmin, self).get_form(request, obj, **kwargs)  # pylint: disable=E1002
        form.current_user = request.user
        return form


class IsDuplicatedFilter(admin.SimpleListFilter):
    """filter items to know if they have a parent"""
    title = _(u'Is duplicated')
    parameter_name = 'duplicated'

    def lookups(self, request, model_admin):
        return [
            (1, _(u'Yes')),
            (2, _(u'No')),
        ]

    def get_duplicate_ids(self, queryset):
        duplicated_ids = []

        for alias in queryset:
            duplicates = models.Alias.objects.filter(path=alias, sites__in=alias.sites.all()).exclude(id=alias.id)
            if duplicates.count() > 0:
                duplicated_ids.append(alias.id)
                duplicated_ids.extend([elt.id for elt in duplicates])
        return duplicated_ids

    def queryset(self, request, queryset):
        value = self.value()
        if value == '1':
            return queryset.filter(id__in=self.get_duplicate_ids(queryset))
        elif value == '2':
            return queryset.exclude(id__in=self.get_duplicate_ids(queryset))
        return queryset


@admin.register(models.Alias)
class AliasAdmin(BASE_ADMIN_CLASS):
    """Alias admin"""
    list_display = ['path', 'redirect_url', 'redirect_code']
    list_editable = ['redirect_url', 'redirect_code']
    list_filter = ['redirect_code', IsDuplicatedFilter, 'sites', ]
    search_fields = ['path', 'redirect_url']
    ordering = ['path', ]
    form = AliasAdminForm


@admin.register(models.MediaFilter)
class MediaFilterAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ImageSize)
class ImageSizeAdmin(admin.ModelAdmin):
    """Image size admin"""
    list_display = ['name', 'size', 'crop']


@admin.register(models.Link)
class LinkAdmin(BASE_ADMIN_CLASS):
    list_display = ('title', 'url', )
    filter_vertical = ('sites', )
    list_filter = ('sites', )
    search_fields = ('title', )


@admin.register(models.PieceOfHtml)
class PieceOfHtmlAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NewsletterSending)
class NewsletterSendingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FragmentType)
class FragmentTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FragmentFilter)
class FragmentFilterAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(BASE_ADMIN_CLASS):
    list_display = ('site', 'homepage_url', 'homepage_article', 'sitemap_mode')

