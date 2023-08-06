from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

from jsonfield import JSONField
from six import python_2_unicode_compatible

from .fields import LimitedMultipleChoiceField, MultipleTextField
from .forms.widgets import LikertSelect, MultiTextWidget, RatingSelect


@python_2_unicode_compatible
class OrdinalScale(models.Model):
    ORDINAL_KIND_LIKERT = "likert"
    ORDINAL_KIND_RATING = "rating"
    ORDINAL_KIND_CHOICES = [
        (ORDINAL_KIND_LIKERT, "Likert Scale"),
        (ORDINAL_KIND_RATING, "Rating Scale")
    ]

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=6, choices=ORDINAL_KIND_CHOICES)

    def __str__(self):
        return "{} [{}]".format(self.name, ", ".join([str(c) for c in self.choices.order_by("score")]))


@python_2_unicode_compatible
class OrdinalChoice(models.Model):
    scale = models.ForeignKey(OrdinalScale, related_name="choices", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    score = models.IntegerField()

    def __str__(self):
        return "{} ({})".format(self.label, self.score)  # pragma: no cover

    class Meta:
        unique_together = [("scale", "score"), ("scale", "label")]


@python_2_unicode_compatible
class Survey(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="surveys", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    published = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated = timezone.now()
        return super(Survey, self).save(*args, **kwargs)

    def __str__(self):
        return self.name  # pragma: no cover

    def get_absolute_url(self):
        return reverse("formly:survey_detail", kwargs={"pk": self.pk})

    def get_run_url(self):
        return reverse("formly:take_survey", kwargs={"pk": self.pk})

    def duplicate(self):  # @@@ This could like use with some refactoring
        survey = Survey.objects.get(pk=self.pk)
        survey.pk = None
        survey.save()
        survey.pages.all().delete()

        pages = {}
        page_targets = []
        choice_targets = []

        for page in Survey.objects.get(pk=self.pk).pages.all():
            orig_page_target = page.target
            orig_page_pk = page.pk
            page.pk = None
            page.survey = survey
            page.target = None
            page.save()
            pages[orig_page_pk] = page
            if orig_page_target:
                page_targets.append({
                    "page": page,
                    "orig_target_pk": orig_page_target.pk
                })
            for field in Page.objects.get(pk=orig_page_pk).fields.all():
                orig_field_pk = field.pk
                field.pk = None
                field.survey = survey
                field.page = page
                field.save()
                for choice in Field.objects.get(pk=orig_field_pk).choices.all():
                    orig_target = choice.target
                    choice.pk = None
                    choice.field = field
                    choice.target = None
                    choice.save()
                    if orig_target:
                        choice_targets.append({
                            "choice": choice,
                            "orig_target_pk": orig_target.pk
                        })

        for page_target in page_targets:
            page = page_target["page"]
            page.target = pages[page_target["orig_target_pk"]]
            page.save()
        for choice_target in choice_targets:
            choice = choice_target["choice"]
            choice.target = pages[choice_target["orig_target_pk"]]
            choice.save()

        return survey

    @property
    def fields(self):
        for page in self.pages.all():
            for field in page.fields.all():
                yield field

    def next_page(self, user):
        return self.first_page().next_page(user=user)

    def first_page(self):
        if self.pages.count() == 0:
            self.pages.create()
        return self.pages.all()[0]

    def publish(self):
        self.published = timezone.now()
        self.save()


@python_2_unicode_compatible
class Page(models.Model):
    survey = models.ForeignKey(Survey, related_name="pages", on_delete=models.CASCADE)
    page_num = models.PositiveIntegerField(null=True, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    # Should be null when a FieldChoice on it's last field has a target.
    target = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = [
            ("survey", "page_num")
        ]
        ordering = ["survey", "page_num"]

    def save(self, *args, **kwargs):
        if self.page_num is None:
            max_page = self.survey.pages.aggregate(Max("page_num"))
            self.page_num = (max_page.get("page_num__max") or 0) + 1
        return super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.label()  # pragma: no cover

    def label(self):
        if self.subtitle:
            return self.subtitle
        else:
            return "Page %d" % self.page_num

    def get_absolute_url(self):
        return reverse("formly:page_detail", kwargs={"pk": self.pk})

    def next_page(self, user):
        target = self

        if self.completed(user=user):
            try:
                target = self.survey.pages.get(
                    page_num=self.page_num + 1
                )
            except Page.DoesNotExist:
                target = None

            if self.target:
                target = self.target

            if target and target.completed(user=user):
                target = target.next_page(user=user)

        return target

    def completed(self, user):
        return self.results.filter(result__user=user).count() > 0

    def is_last_page(self):
        return self.next_page() is None


@python_2_unicode_compatible
class Field(models.Model):
    TEXT_FIELD = 0
    TEXT_AREA = 1
    RADIO_CHOICES = 2
    DATE_FIELD = 3
    SELECT_FIELD = 4
    CHECKBOX_FIELD = 5
    MEDIA_FIELD = 6
    BOOLEAN_FIELD = 7
    MULTIPLE_TEXT = 8
    LIKERT_FIELD = 9
    RATING_FIELD = 10

    FIELD_TYPE_CHOICES = [
        (TEXT_FIELD, "Free Response - One Line"),
        (TEXT_AREA, "Free Response - Box"),
        (RADIO_CHOICES, "Multiple Choice - Pick One"),
        (SELECT_FIELD, "Multiple Choice - Pick One (Dropdown)"),
        (CHECKBOX_FIELD, "Multiple Choice - Can select multiple answers"),
        (DATE_FIELD, "Date"),
        (MEDIA_FIELD, "File Upload"),
        (BOOLEAN_FIELD, "True/False"),
        (MULTIPLE_TEXT, "Multiple Free Responses - Single Lines"),
        (LIKERT_FIELD, "Likert Scale"),
        (RATING_FIELD, "Rating Scale")
    ]

    survey = models.ForeignKey(Survey, related_name="fields", on_delete=models.CASCADE)  # Denorm
    page = models.ForeignKey(Page, null=True, blank=True, related_name="fields", on_delete=models.SET_NULL)
    label = models.TextField()
    field_type = models.IntegerField(choices=FIELD_TYPE_CHOICES)
    scale = models.ForeignKey(OrdinalScale, default=None, null=True, blank=True, related_name="fields", on_delete=models.SET_NULL)
    help_text = models.TextField(blank=True)
    ordinal = models.IntegerField()
    maximum_choices = models.IntegerField(null=True, blank=True)
    # Should this be moved to a separate Constraint model that can also
    # represent cross field constraints
    required = models.BooleanField(default=False)
    expected_answers = models.PositiveSmallIntegerField(default=1)

    mapping = JSONField(blank=True, default=dict())

    # def clean(self):
    #     super(Field, self).clean()
    #     if self.page is None:
    #         if self.target_choices.count() == 0:
    #             raise ValidationError(
    #                 "A question not on a page must be a target of a choice from another question"
    #             )

    def save(self, *args, **kwargs):
        if not self.ordinal:
            # Set ordinal, since full_clean() will fail if not set
            self.ordinal = 1
        self.full_clean()
        if not self.pk and self.page is not None:
            self.ordinal = (self.page.fields.aggregate(
                Max("ordinal")
            )["ordinal__max"] or 0) + 1
        return super(Field, self).save(*args, **kwargs)

    def move_up(self):
        try:
            other_field = self.page.fields.order_by("-ordinal").filter(
                ordinal__lt=self.ordinal
            )[0]
            existing = self.ordinal
            other = other_field.ordinal
            self.ordinal = other
            other_field.ordinal = existing
            other_field.save()
            self.save()
        except IndexError:
            return

    def move_down(self):
        try:
            other_field = self.page.fields.order_by("ordinal").filter(
                ordinal__gt=self.ordinal
            )[0]
            existing = self.ordinal
            other = other_field.ordinal
            self.ordinal = other
            other_field.ordinal = existing
            other_field.save()
            self.save()
        except IndexError:
            return

    class Meta:
        ordering = ["ordinal"]

    def __str__(self):
        return "%s of type %s on %s" % (
            self.label, self.get_field_type_display(), self.survey
        )

    def get_absolute_url(self):
        return reverse("formly:field_update", kwargs={"pk": self.pk})

    @property
    def needs_choices(self):
        return self.field_type in [
            Field.RADIO_CHOICES,
            Field.SELECT_FIELD,
            Field.CHECKBOX_FIELD
        ]

    @property
    def name(self):
        return slugify(self.label)

    @property
    def is_multiple(self):
        return self.field_type == Field.MULTIPLE_TEXT

    def form_field(self):
        if self.field_type in [Field.LIKERT_FIELD, Field.RATING_FIELD]:
            if self.scale:
                choices = [(x.pk, x.label) for x in self.scale.choices.all().order_by("score")]
            else:
                choices = []
        else:
            choices = [(x.pk, x.label) for x in self.choices.all()]

        field_class, field_kwargs = self._get_field_class(choices)
        field = field_class(**field_kwargs)
        return field

    def _get_field_class(self, choices):
        """
        Set field_class and field kwargs based on field type
        """
        field_class = forms.CharField
        kwargs = dict(
            label=self.label,
            help_text=self.help_text,
            required=self.required
        )
        field_type = FIELD_TYPES.get(self.field_type, {})
        field_class = field_type.get("field_class", field_class)
        kwargs.update(**field_type.get("kwargs", {}))

        if self.field_type in [Field.CHECKBOX_FIELD, Field.SELECT_FIELD, Field.RADIO_CHOICES, Field.LIKERT_FIELD, Field.RATING_FIELD]:
            kwargs.update({"choices": choices})
            if self.field_type == Field.CHECKBOX_FIELD:
                kwargs.update({"maximum_choices": self.maximum_choices})
        elif self.field_type == Field.MULTIPLE_TEXT:
            kwargs.update({
                "fields_length": self.expected_answers,
                "widget": MultiTextWidget(widgets_length=self.expected_answers),
            })
        return field_class, kwargs


FIELD_TYPES = {
    Field.TEXT_AREA: dict(
        field_class=forms.CharField,
        kwargs=dict(
            widget=forms.Textarea
        )
    ),
    Field.RADIO_CHOICES: dict(
        field_class=forms.ChoiceField,
        kwargs=dict(
            widget=forms.RadioSelect
        )
    ),
    Field.LIKERT_FIELD: dict(
        field_class=forms.ChoiceField,
        kwargs=dict(
            widget=LikertSelect
        )
    ),
    Field.RATING_FIELD: dict(
        field_class=forms.ChoiceField,
        kwargs=dict(
            widget=RatingSelect
        )
    ),
    Field.DATE_FIELD: dict(
        field_class=forms.DateField,
        kwargs=dict()
    ),
    Field.SELECT_FIELD: dict(
        field_class=forms.ChoiceField,
        kwargs=dict(
            widget=forms.Select
        )
    ),
    Field.CHECKBOX_FIELD: dict(
        field_class=LimitedMultipleChoiceField,
        kwargs=dict(
            widget=forms.CheckboxSelectMultiple
        )
    ),
    Field.BOOLEAN_FIELD: dict(
        field_class=forms.BooleanField,
        kwargs=dict()
    ),
    Field.MEDIA_FIELD: dict(
        field_class=forms.FileField,
        kwargs=dict()
    ),
    Field.MULTIPLE_TEXT: dict(
        field_class=MultipleTextField,
        kwargs=dict()
    )
}


@python_2_unicode_compatible
class FieldChoice(models.Model):
    field = models.ForeignKey(Field, related_name="choices", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    target = models.ForeignKey(Field, null=True, blank=True, related_name="target_choices", on_delete=models.SET_NULL)

    def clean(self):
        super(FieldChoice, self).clean()
        if self.target is not None:
            if self.target.page:
                raise ValidationError(
                    "FieldChoice target's can only be questions not associated with a page."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(FieldChoice, self).save(*args, **kwargs)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class SurveyResult(models.Model):
    survey = models.ForeignKey(Survey, related_name="survey_results", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="survey_results", on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("survey_edit", kwargs={"pk": self.pk, "page": 1})

    def __str__(self):
        return self.survey.name


@python_2_unicode_compatible
class FieldResult(models.Model):
    survey = models.ForeignKey(Survey, related_name="results", on_delete=models.CASCADE)  # Denorm
    page = models.ForeignKey(Page, related_name="results", on_delete=models.CASCADE)  # Denorm
    result = models.ForeignKey(SurveyResult, related_name="results", on_delete=models.CASCADE)
    question = models.ForeignKey(Field, related_name="results", on_delete=models.CASCADE)
    upload = models.FileField(upload_to="formly/", blank=True)
    answer = JSONField(blank=True)  # @@@ I think this should be something different than a string

    def _update_mapping(self):
        answer = self.answer["answer"]
        mapping = dict()
        for ans in answer:
            ans = ans.strip().upper()
            if ans in self.question.mapping:
                mapping[ans] = self.question.mapping[ans]
        self.answer["mapping"] = mapping

    def save(self, *args, **kwargs):
        if self.question.field_type == Field.MULTIPLE_TEXT:
            self._update_mapping()
        return super(FieldResult, self).save(*args, **kwargs)

    def answer_value(self):
        if self.answer:
            return self.answer.get("answer")

    def answer_display(self):
        val = self.answer_value()
        if val:
            if self.question.needs_choices:
                if self.question.field_type == Field.CHECKBOX_FIELD:
                    return ", ".join([str(FieldChoice.objects.get(pk=int(v))) for v in val])
                return FieldChoice.objects.get(pk=int(val)).label
            if self.question.field_type in [Field.LIKERT_FIELD, Field.RATING_FIELD]:
                choice = OrdinalChoice.objects.get(pk=int(val))
                return "{} ({})".format(choice.label, choice.score)
        return val

    def __str__(self):
        return self.survey.name

    class Meta:
        ordering = ["result", "question"]
