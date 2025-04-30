from django.urls import path
from . import views

# urlpatterns = [
#     path('api/basicDetails/',views.AddBasicDetails, name='AddBasicDetails'),
#     path('api/basicDetails/<int:id>/',views.AddBasicDetails, name='AddBasicDetails'),
#     path('api/addExperience/', views.AddExperience, name='AddExperience'),
#     path('api/getExperienceData/<int:id>', views.AddExperience, name='AddExperience'),
#     path('api/addProjects/', views.AddProject, name='AddProject'),
#     path('api/addSkills/', views.Skills, name='Skills'),
#     path('api/addSkills/<int:id>/', views.Skills, name='Skills'),
#     path('api/addEducation/', views.Education, name='Education'),
#     path('api/addEducation/<int:id>/', views.Education, name='education_id'),
#     path('api/getResumeData/', views.GetResumeData, name='GetResumeData')
# ]

urlpatterns = [
    
    path('register/', views.register_view),
    path('login/', views.login_view, name='login'),
    
    
    path('api/basicDetails/', views.AddBasicDetails, name='AddBasicDetails'),
    path('api/basicDetails/<int:id>/', views.AddBasicDetails, name='UpdateDeleteBasicDetails'),

    
    path('api/addExperience/', views.AddExperience, name='AddExperience'),
    path('api/addExperience/<int:id>/', views.AddExperience, name='UpdateDeleteExperience'),

    
    path('api/addProjects/', views.AddProject, name='AddProject'),
    path('api/addProjects/<int:id>/', views.AddProject, name='UpdateDeleteProject'),

    
    path('api/addSkills/', views.skills_view, name='AddSkill'),
    path('api/addSkills/<int:id>/', views.skills_view, name='UpdateDeleteSkill'),

    
    path('api/addEducation/', views.AddEducation, name='AddEducation'),
    path('api/addEducation/<int:id>/', views.AddEducation, name='UpdateDeleteEducation'),

    
    path('api/getResumeData/', views.GetResumeData, name='GetResumeData')
]
