from django.conf import settings

def ANUTheme(context):
    """Injects the ANU settings dictionary into the context"""
    return {'ANU': settings.ANU}
