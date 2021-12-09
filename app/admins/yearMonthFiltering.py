from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class YearListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('année')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'année'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('2022', _('2022 et après')),
            ('2021', _('2021')),
            ('2020', _('2020')),
            ('2019', _('2019 et avant')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '2022':
            return queryset.filter(stop_dat__gte='2022')
        if self.value() == '2021':
            return queryset.filter(stop_dat__startswith='2021')
        if self.value() == '2020':
            return queryset.filter(stop_dat__startswith='2020')
        if self.value() == '2019':
            return queryset.filter(stop_dat__lte='2020-13')


class MonthListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('mois')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'mois'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('01', _('Janvier')),
            ('02', _('Février')),
            ('03', _('Mars')),
            ('04', _('Avril')),
            ('05', _('Mai')),
            ('06', _('Juin')),
            ('07', _('Juillet')),
            ('08', _('Août')),
            ('09', _('Septembre')),
            ('10', _('Octobre')),
            ('11', _('Novembre')),
            ('12', _('Décembre')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '01':
            return queryset.filter(stop_dat__contains='-01-')
        if self.value() == '02':
            return queryset.filter(stop_dat__contains='-02-')
        if self.value() == '03':
            return queryset.filter(stop_dat__contains='-03-')
        if self.value() == '04':
            return queryset.filter(stop_dat__contains='-04-')
        if self.value() == '05':
            return queryset.filter(stop_dat__contains='-05-')
        if self.value() == '06':
            return queryset.filter(stop_dat__contains='-06-')
        if self.value() == '07':
            return queryset.filter(stop_dat__contains='-07-')
        if self.value() == '08':
            return queryset.filter(stop_dat__contains='-08-')
        if self.value() == '09':
            return queryset.filter(stop_dat__contains='-09-')
        if self.value() == '10':
            return queryset.filter(stop_dat__contains='-10-')
        if self.value() == '11':
            return queryset.filter(stop_dat__contains='-11-')
        if self.value() == '12':
            return queryset.filter(stop_dat__contains='-12-')
