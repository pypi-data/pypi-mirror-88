from helper import HELPER_SETTINGS

HELPER_SETTINGS["TEMPLATE_CONTEXT_PROCESSORS"] = ["django.core.context_processors.debug"]
HELPER_SETTINGS["TEST_RUNNER"] = "runners.CapturedOutputRunner"
HELPER_SETTINGS["INSTALLED_APPS"].remove("djangocms_text_ckeditor")
