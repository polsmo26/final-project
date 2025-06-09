from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile
from tasks.models import Task

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('title', 'description', 'completed', 'difficulty')
    readonly_fields = ('created_at',)

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'
    fields = ('school', 'grade_level', 'birthdate', 'town', 'parent_contact')

class CustomUserAdmin(UserAdmin):
    inlines = (StudentProfileInline, TaskInline)
    list_display = ('username', 'email', 'is_student', 'get_school', 'get_grade', 'get_birthdate', 'get_town')
    list_select_related = ('studentprofile',)
    
    def get_school(self, instance):
        return instance.studentprofile.school if hasattr(instance, 'studentprofile') else None
    get_school.short_description = 'School'

    def get_grade(self, instance):
        return instance.studentprofile.grade_level if hasattr(instance, 'studentprofile') else None
    get_grade.short_description = 'Grade'

    def get_birthdate(self, instance):
        return instance.studentprofile.birthdate if hasattr(instance, 'studentprofile') else None
    get_birthdate.short_description = 'Birthdate'

    def get_town(self, instance):
        return instance.studentprofile.town if hasattr(instance, 'studentprofile') else None
    get_town.short_description = 'Town'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# This should be outside the class definition
admin.site.register(User, CustomUserAdmin)

