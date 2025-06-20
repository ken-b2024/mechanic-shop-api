from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
ma = Marshmallow()

limiter = Limiter(key_func=get_remote_address,
                  default_limits=['100 per day', '50 per hour']
                )

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})