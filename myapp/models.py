from django.db import models
from django.core.exceptions import ValidationError


class DataRow(models.Model):
    # department_code = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
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
    last_change_date = models.DateTimeField(auto_now=True)  # auto_now makes it non-editable
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
        # Ensure that the fields are cast to float, defaulting to 0 if they are None or empty
        self.divisible = sum(filter(None, [
            float(self.kinnaur or 0),
            float(self.lahaul or 0),
            float(self.spiti or 0),
            float(self.pangi or 0),
            float(self.bharmaur or 0)
        ]))

        # Ensure that in_divisible and revised_estimate are treated as floats
        self.revised_estimate = sum(filter(None, [
            float(self.in_divisible or 0),
            self.divisible  # already a float value
        ]))

        # Ensure sanctioned_budget is a float
        self.sanctioned_budget = float(self.sanctioned_budget or 0)

        # Auto-calculate Excess, Surrender, and Variation
        if self.revised_estimate > self.sanctioned_budget:
            self.excess = self.revised_estimate - self.sanctioned_budget
            self.surrender = 0
        else:
            self.surrender = self.sanctioned_budget - self.revised_estimate
            self.excess = 0
        
        # Calculate Variation as the difference between revised_estimate and surrender
        self.variation = self.revised_estimate - self.surrender

        # Auto-generate unique_search field
        self.unique_search = f"{self.department_name}-{self.scheme_name}-{self.head_name}-{self.soe_name}"

        # Call full_clean for validation
        self.full_clean()

        # Save the object
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
