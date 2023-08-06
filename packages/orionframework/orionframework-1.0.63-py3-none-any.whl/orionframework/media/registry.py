from orionframework.utils.reflection import require
from django.contrib import admin as django_admin


class MediaRegistry(object):
    defaults = {
        "document": {
            "serializer": "orionframework.media.document.serializers.DocumentSerializer",
            "service": "orionframework.media.document.services.ServiceDocument",
            "admin": "orionframework.media.document.admin.DocumentAdmin"
        },
        "online-document": {
            "serializer": "orionframework.media.online_document.serializers.OnlineDocumentSerializer",
            "service": "orionframework.media.online_document.services.ServiceOnlineDocument",
            "admin": "orionframework.media.online_document.admin.OnlineDocumentAdmin"
        },
        "image": {
            "serializer": "orionframework.media.image.serializers.ImageSerializer",
            "service": "orionframework.media.image.services.ServiceImage",
            "admin": "orionframework.media.image.admin.ImageAdmin"
        }
    }

    def __init__(self, storage=[]):
        self.storage = {}

        for entry in storage:
            self.add(**entry)

    def add(self, model, serializer=None, service=None, admin=None, **kwargs):
        model = require(model)

        default = self.defaults.get(model.type, {})

        serializer = serializer or default.get("serializer")
        service = service or default.get("service")
        admin = admin or default.get("admin")

        # if model and admin:
        #    django_admin.site.register(model, admin)

        self.storage[model.type] = {
            "model": model,
            "serializer": serializer,
            "service": service,
            "admin": admin,
            **kwargs
        }

    def get_model(self, media_type):
        return self.storage.get(media_type, {}).get("model")

    def get_admin(self, media_type):
        entry = self.storage.get(media_type, {})
        admin = entry.get("admin")

        if isinstance(admin, str):
            admin = require(admin)
            entry["admin"] = admin

        return admin

    def get_serializer(self, media_type):
        entry = self.storage.get(media_type, {})
        serializer = entry.get("serializer")

        if isinstance(serializer, str):
            serializer = require(serializer)
            entry["serializer"] = serializer

        return serializer

    def get_service(self, media_type):
        entry = self.storage.get(media_type, {})
        service = entry.get("service")

        if isinstance(service, str):
            service = require(service)
            entry["service"] = service

        return service

    def register_admin(self, site):
        for media_type in self.storage.keys():
            model = self.get_model(media_type)
            admin = self.get_admin(media_type)
            if admin:
                site.register(model, admin)
