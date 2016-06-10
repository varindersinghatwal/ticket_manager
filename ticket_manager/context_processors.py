from ticket_manager.settings import SITE_TITLE, SITE_LOGO_NAME

def custom_context_processor(request):
   return {'SITE_TITLE': SITE_TITLE, 'SITE_LOGO_NAME': SITE_LOGO_NAME}
