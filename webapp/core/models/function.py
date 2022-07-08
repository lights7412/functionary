""" Function model """
import uuid

from django.db import models


class Function(models.Model):
    """Function is a unit of work that can be tasked

    Attributes:
        id: unique identifier (UUID)
        package: the package that the function is a part of
        name: internal name that published package definition keys off of
        display_name: optional display name
        description: more details about the function
        schema: the function's OpenAPI definition
        active: whether this function is the one that is taskable. False indicates that
                this is a historical entry.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    package = models.ForeignKey(to="Package", on_delete=models.CASCADE)

    # TODO: This shouldn't be changeable after creation
    name = models.CharField(max_length=64, blank=False)

    display_name = models.CharField(max_length=64, null=True)
    description = models.TextField(null=True)
    schema = models.JSONField()

    # TODO: Add validation so that only one entry sharing a package and name can be
    #       active
    active = models.BooleanField(default=True, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["package", "name"], name="package_name_unique_together"
            )
        ]
        indexes = [
            models.Index(
                fields=["package", "active"],
                condition=models.Q(active=True),
                name="package_active_true_index",
            )
        ]

    def __str__(self):
        return self.name
