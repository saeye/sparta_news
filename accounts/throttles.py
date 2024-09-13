from rest_framework.throttling import UserRateThrottle

class UpdateRateThrottle(UserRateThrottle):
    scope = 'update'
