from django.contrib import admin

from .models import ImportSetup, ImportSetupAction, ImportSetupItem


class ImportSetupItemInline(admin.StackedInline):
    model = ImportSetupItem
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class ImportSetupActionInline(admin.StackedInline):
    model = ImportSetupAction
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


@admin.register(ImportSetup)
class ImportSetupAdmin(admin.ModelAdmin):
    inlines = (ImportSetupActionInline, ImportSetupItemInline,)
    list_display = (
        'label', 'document_type', 'credential', 'process_size'
    )
