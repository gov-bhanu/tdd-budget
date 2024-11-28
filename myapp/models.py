from django.db import models
from django.core.exceptions import ValidationError


class DataRow(models.Model):
    # department_code = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    head_name = models.CharField(max_length=100)
    scheme_name = models.CharField(max_length=150)
    soe_name = models.CharField(max_length=100)
    sanctioned_budget = models.FloatField()
    revised_estimate = models.FloatField(null=True, blank=True)
    in_divisible = models.FloatField(null=True, blank=True)
    divisible = models.FloatField(null=True, blank=True)
    kinnaur = models.FloatField(null=True, blank=True)
    lahaul = models.FloatField(null=True, blank=True)
    spiti = models.FloatField(null=True, blank=True)
    pangi = models.FloatField(null=True, blank=True)
    bharmaur = models.FloatField(null=True, blank=True)
    excess = models.FloatField(null=True, blank=True)
    surrender = models.FloatField(null=True, blank=True)
    variation = models.FloatField(null=True, blank=True)
    agreed_by_fd = models.FloatField(null=True, blank=True)
    unique_search = models.CharField(max_length=255, unique=True, editable=False)



    # Ensure soe_name is unique under a specific head_name
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["soe_name", "head_name"],
                name="unique_soe_per_head"
            ),
        ]

    def save(self, *args, **kwargs):
        # Auto-calculate revised_estimate
        self.divisible = sum(filter(None, [self.kinnaur, self.lahaul, self.spiti, self.pangi, self.bharmaur]))
        self.revised_estimate = sum(filter(None, [self.in_divisible, self.divisible]))

        # Auto-calculate Excess, Surrender, and Variation
        if self.revised_estimate > self.sanctioned_budget:
            self.excess = self.revised_estimate - self.sanctioned_budget
            self.surrender = 0
        else:
            self.surrender = self.sanctioned_budget - self.revised_estimate
            self.excess = 0
        
        # Calculate Variation as difference between revised_estimate and surrender
        self.variation = self.revised_estimate - self.surrender

        # Auto-generate unique_search field
        # self.unique_search = f"{self.department_code}-{self.department_name}-{self.scheme_name}-{self.head_name}-{self.soe_name}"
        self.unique_search = f"{self.type}-{self.department_name}-{self.scheme_name}-{self.head_name}-{self.soe_name}"

        # Call full_clean for validation
        self.full_clean()

        super().save(*args, **kwargs)


    def clean(self):
        # # Ensure department_code is tied to the same department_name across rows
        # existing = DataRow.objects.filter(department_code=self.department_code).exclude(id=self.id)
        # if existing.exists() and existing.first().department_name != self.department_name:
        #     raise ValidationError("The department_code is already assigned to a different department_name.")
        
        # Ensure head_name is tied to the same department_name
        existing_head = DataRow.objects.filter(head_name=self.head_name).exclude(id=self.id)
        if existing_head.exists() and existing_head.first().department_name != self.department_name:
            raise ValidationError(f"The Head Name '{self.head_name}' is already assigned to a different Department Name: '{self.department_name}'.")
        
        super().clean()

    def __str__(self):
        return f"{self.head_name} - {self.soe_name} ({self.unique_search})"
