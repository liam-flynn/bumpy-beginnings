from django.shortcuts import redirect

# Middleware to redirect users to the 'get_details' page if they are missing SiteUser details.


class RequireDetailsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            # Check the session flag
            if request.session.pop('requires_details', False):
                # Redirect to the details page
                return redirect('get_details')
        return self.get_response(request)
