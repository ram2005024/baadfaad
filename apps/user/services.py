from django.core.cache import cache


class VerificationService:
    CODE_TTL=300
    ATTEMPT_TTL=600
    MAX_ATTEMPT_COUNT=5
    @staticmethod
    def _verification_key(user_id):
        return f"user:{user_id}:code"

    @staticmethod
    def _attempt_key(user_id):
        return f"user:{user_id}:attempts"

    @classmethod
    def save_verification_code(cls,user_id,code):
        cache.set(cls._verification_key(user_id),code,cls.CODE_TTL)

    @classmethod
    def is_verification_expired(cls,user_id):
        key=cls._verification_key(user_id)
        return cache.get(key)

    @classmethod
    def set_attempt(cls,user_id):
        cache.set(cls._attempt_key(user_id),1,timeout=cls.ATTEMPT_TTL)

    @classmethod
    def has_attempt_exceeded(cls,user_id):
        has_attempt=cache.get(cls._attempt_key(user_id))
        if has_attempt:
            if has_attempt>cls.MAX_ATTEMPT_COUNT:
                return True
        return False

    @classmethod
    def increase_attempt(cls,user_id):
        if cache.get(cls._attempt_key(user_id)):
            cache.incr(key=cls._attempt_key(user_id),delta=1)
        else:
            cls.set_attempt(user_id)
            cache.incr(key=cls._attempt_key(user_id), delta=1)



