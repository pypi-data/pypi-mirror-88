from rest_framework.renderers import BrowsableAPIRenderer

__all__ = ("BrowsableAPIRendererWithoutForms",)


class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context["display_edit_forms"] = False
        return context

    def show_form_for_method(self, view, method, request, obj):
        return False

    def get_rendered_html_form(self, data, view, method, request):
        return None

    def get_raw_data_form(self, data, view, method, request):
        return None

    def get_filter_form(self, data, view, request):
        return None
