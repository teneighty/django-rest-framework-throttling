from rest_framework.throttling import UserRateThrottle
from rest_framework_throttling.models import UserThrottleRules

class PerUserThrottle(UserRateThrottle):
    scope = 'per_user_throttle'

    def allow_request(self, request, view):
        if request.user.is_authenticated():
            self.__set_user_rate__(request.user, view)
        return super(PerUserThrottle, self).allow_request(request, view)

    def __set_user_rate__(self, user, view):
        try:
            r = UserThrottleRules.objects.get(user=user, view=self.__view_name__(view))
            self.rate = r.rate
            self.num_requests, self.duration = self.parse_rate(self.rate)
        except UserThrottleRules.DoesNotExist:
            try:
                r = UserThrottleRules.objects.get(user=user, view='*')
                self.rate = r.rate
                self.num_requests, self.duration = self.parse_rate(self.rate)
            except UserThrottleRules.DoesNotExist:
                pass

    def __view_name__(self, view):
        return view.__module__ + "." + view.__class__.__name__
