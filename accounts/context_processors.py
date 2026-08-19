def user_role_context(request):
    context = {
        'is_student_verified': False,
        'is_therapist': False,
        'therapist_profile': None,
        'student_verification': None,
    }
    if request.user.is_authenticated:
        if hasattr(request.user, 'therapist_profile'):
            context['is_therapist'] = True
            context['therapist_profile'] = request.user.therapist_profile
        if hasattr(request.user, 'student_verification'):
            context['student_verification'] = request.user.student_verification
            context['is_student_verified'] = request.user.student_verification.is_verified
    return context
