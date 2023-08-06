from sregistry.defaults import SREGISTRY_DATABASE

if SREGISTRY_DATABASE is None:
    from .dummy import add, init_db
else:
    from .models import Collection, Container, init_db, Base
    from .sqlite import (
        add,
        cp,
        get,
        mv,
        rm,
        images,
        inspect,
        get_container,
        get_collection,
        get_or_create_collection,
        rename,
    )
