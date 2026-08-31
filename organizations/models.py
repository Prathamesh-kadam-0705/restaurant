from django.db import models

from django.conf import settings


class Organization(models.Model):

    name = models.CharField(max_length = 150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Branch(models.Model):

    name = models.CharField(max_length=150)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )
    address = models.CharField(max_length = 250)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrganizationMembership(models.Model):

    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )
    role = models.CharField(max_length= 10,choices=[
        ('OWNER', 'Owner'),
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff'),
    ])
    branch_access = models.ManyToManyField(Branch)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','organization'],
                name="unique_user_organization_membership"
            )
        ]

    def add_branch(self,branch):
        if self.organization == branch.organization:
           self.branch_access.add(branch)
           return True

        return False
