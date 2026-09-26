from django.core.cache import cache
from sqlparse.utils import offset

from config.redis import redis


class VerificationService:
    CODE_TTL = 300
    ATTEMPT_TTL = 600
    MAX_ATTEMPT_COUNT = 5
    RESEND_TTL = 60
    RESET_TTL=3600



    @staticmethod
    def _verification_key(user_id):
        return f"user:{user_id}:code"

    @staticmethod
    def _reset_key(user_id):
        return f"user:{user_id}:reset"

    @staticmethod
    def _attempt_key(user_id):
        return f"user:{user_id}:attempts"

    @staticmethod
    def _resend_key(user_id):
        return f"user:{user_id}:resend"

    @classmethod
    def save_verification_code(cls, user_id, code):
        redis.set(cls._verification_key(user_id), code, cls.CODE_TTL)

    @classmethod
    def has_sent_verification_code(cls, user_id):
        key = cls._verification_key(user_id)
        return redis.get(key)

    @classmethod
    def check_verification_code(cls, code, user_id):
        value = cls.has_sent_verification_code(user_id)
        print(f"{value} and my code is {code}")
        if value:
            is_matched = code == value
            if is_matched:
                redis.delete(cls._attempt_key(user_id))
                redis.delete(cls._verification_key(user_id))
                return True
        cls.increase_attempt(user_id)
        return False

    @classmethod
    def set_attempt(cls, user_id):
        redis.set(cls._attempt_key(user_id), 0, ex=cls.ATTEMPT_TTL)

    @classmethod
    def has_attempt_exceeded(cls, user_id):
        has_attempt = redis.get(cls._attempt_key(user_id))
        if has_attempt:
            return int(has_attempt) > cls.MAX_ATTEMPT_COUNT
        return False

    @classmethod
    def increase_attempt(cls, user_id):
        if redis.get(cls._attempt_key(user_id)):
            redis.incr(cls._attempt_key(user_id))
        else:
            cls.set_attempt(user_id)
            redis.incr(name=cls._attempt_key(user_id))

    @classmethod
    def has_resend_key(cls, user_id):
        key = cls._resend_key(user_id)
        value = redis.get(key)
        if not value:
            return None, 0
        ttl = redis.ttl(key)
        if ttl <= 0:
            print(key)
            print(redis.keys("*"))
            print(redis.get(key))
            print(ttl, "Yaha xa hai brooooo")
            return value, 0
        return value, ttl

    @classmethod
    def set_resend_key(cls, user_id):
        return redis.set(cls._resend_key(user_id), str(True), cls.RESEND_TTL)

    @classmethod
    def has_reset_sent(cls,user_id):
        key=cls._reset_key(user_id)
        return redis.get(key)

    @classmethod
    def set_reset_key(cls,user_id,token):
        keyword=cls._reset_key(user_id)
        return redis.set(keyword,token.encode(),cls.RESET_TTL)

    @classmethod
    def delete_reset_key(cls,user_id):
        key=cls._reset_key(user_id)
        if redis.get(key):
            redis.delete(key)