from django.shortcuts import redirect


def login_required(view_func):
    def wrapped_func(requests, *args, **kwargs):
        if not requests.session.get('user_email'):
            return redirect('home')  # Redirect to your custom login page

        return view_func(requests, *args, **kwargs)
    return wrapped_func


def logged_in(view_func):
    def wrapped_func(requests, *args, **kwargs):
        if requests.session.get('user_email'):
            return redirect('bot')  # Redirect to your custom login page

        return view_func(requests, *args, **kwargs)
    return wrapped_func
