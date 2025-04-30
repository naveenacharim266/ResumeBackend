from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from .models import BasicDetails, Experience, Education, Project, Skills, Certifications
from django.contrib.auth.models import User
import pdb

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'status': 'success', 'message': 'User registered successfully'}, status=201)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                return JsonResponse({'status': 'success', 'message': 'Login successful', 'user_id': user.id})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)
        
def get_user_from_request(request, data=None):
    user_id = (
        request.GET.get("user_id")
        or (data or {}).get("user")
        or (data or {}).get("userId")
    )
    if not user_id:
        raise ValueError("Missing user_id")
    return User.objects.get(id=user_id)


@csrf_exempt
def AddBasicDetails(request, id=None):
    if request.GET.get('user_id') != '' :
        id = request.GET.get('user_id')

    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            try:
                user_instance = User.objects.get(id=data.get('user'))
                basicdetails, created = BasicDetails.objects.update_or_create(
                    user=user_instance,
                    defaults={
                        'name': data.get('name'),
                        'email': data.get('email'),
                        'phone': data.get('phone'),
                        'summary': data.get('summary'),
                        'linkedin': data.get('linkedin'),
                        'github': data.get('github'),
                        'website': data.get('website'),
                    }
                )
                return JsonResponse({
                    "status": "success",
                    "id": basicdetails.id,
                    "created": created
                }, status=201)

            except User.DoesNotExist:
                return JsonResponse({"status": "error", "message": "User not found."}, status=404)

        elif request.method == 'GET':
            # READ basic details
            
            if id:
                try:
                    basic = BasicDetails.objects.get(id=id)
                    basic_data = {
                        #'id': basic.id,
                        'name': basic.name,
                        'email': basic.email,
                        'phone': basic.phone,
                        'summary': basic.summary,
                        'linkedin': basic.linkedin,
                        'github': basic.github,
                        'website': basic.website,
                    }
                    return JsonResponse({'status': 'success', 'basicdetails': basic_data}, status=200)
                except BasicDetails.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'BasicDetails not found'}, status=404)
            else:
                basics = BasicDetails.objects.all().values()
                return JsonResponse({'status': 'success', 'basicdetails': list(basics)}, status=200)

        elif request.method == 'PUT':
            if not id:
                return JsonResponse({'status': 'error', 'message': 'ID is required for update'}, status=400)
            data = json.loads(request.body)
            try:
                basic = BasicDetails.objects.get(id=id)
                basic.name = data.get('name', basic.name)
                basic.email = data.get('email', basic.email)
                basic.phone = data.get('phone', basic.phone)
                basic.summary = data.get('summary', basic.summary)
                basic.linkedin = data.get('linkedin', basic.linkedin)
                basic.github = data.get('github', basic.github)
                basic.website = data.get('website', basic.website)
                basic.save()
                return JsonResponse({'status': 'success', 'message': 'Basic details updated successfully'}, status=200)
            except BasicDetails.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'BasicDetails not found'}, status=404)

        elif request.method == 'DELETE':
            # DELETE basic details
            if not id:
                return JsonResponse({'status': 'error', 'message': 'ID is required for delete'}, status=400)
            try:
                basic = BasicDetails.objects.get(id=id)
                basic.delete()
                return JsonResponse({'status': 'success', 'message': 'Basic details deleted successfully'}, status=200)
            except BasicDetails.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'BasicDetails not found'}, status=404)

        else:
            return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
@csrf_exempt
def AddExperience(request, id=None):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            user = get_user_from_request(request, data)

            Experience.objects.create(
                user=user,
                title=data.get("title"),
                employment_type=data.get("employment_type"),
                organization=data.get("organization"),
                startdate=data.get("startdate"),
                enddate=data.get("enddate"),
                location=data.get("location"),
                location_type=data.get("location_type"),
                description=data.get("description"),
                skills_used=data.get("skills_used"),
            )
            return JsonResponse({"status": "success", "message": "Saved Successfully"})

        elif request.method == "GET":
            #pdb.set_trace()
            user = get_user_from_request(request)
            if id:
                experience = Experience.objects.get(id=id, user=user)
                experience_data = {field.name: getattr(experience, field.name) for field in experience._meta.fields if field.name != 'user'}
                return JsonResponse({"status": "success", "data": experience_data})
            else:
                experiences = Experience.objects.filter(user=user)
                return JsonResponse({"status": "success", "data": list(experiences.values())})

        elif request.method == "PUT":
            data = json.loads(request.body)
            experience = Experience.objects.get(id=id)
            for field in ['title', 'employment_type', 'organization', 'startdate', 'enddate', 'location', 'location_type', 'description', 'skills_used']:
                if field in data:
                    setattr(experience, field, data[field])
            experience.save()
            return JsonResponse({"status": "success", "message": "Updated"})

        elif request.method == "DELETE":
            Experience.objects.get(id=id).delete()
            return JsonResponse({"status": "success", "message": "Deleted"})

        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@csrf_exempt
def AddProject(request, id=None):
    try:
        user_id = request.GET.get('user_id')
        if request.method == 'POST':
            data = json.loads(request.body)
            try:
                user = User.objects.get(id=data.get('user'))
                Project.objects.create(
                    user=user,
                    project_title=data.get('project_title'),
                    role=data.get('role'),
                    client=data.get('client'),
                    startdate=data.get('startdate'),
                    enddate=data.get('enddate'),
                    project_details=data.get('project_details')
                )
                return JsonResponse({'status': 'success', 'message': 'Project saved successfully!'}, status=201)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

        elif request.method == 'GET':
            if not user_id:
                return JsonResponse({'status': 'error', 'message': 'Missing user_id'}, status=400)
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

            if id:
                try:
                    project = Project.objects.get(id=id, user=user)
                    project_data = {
                        'id': project.id,
                        'project_title': project.project_title,
                        'role': project.role,
                        'client': project.client,
                        'startdate': project.startdate,
                        'enddate': project.enddate,
                        'project_details': project.project_details
                    }
                    return JsonResponse({'status': 'success', 'data': project_data}, status=200)
                except Project.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)
            else:
                projects = Project.objects.filter(user=user)
                project_list = list(projects.values())
                return JsonResponse({'status': 'success', 'data': project_list}, status=200)

        elif request.method == 'PUT':
            if not id:
                return JsonResponse({'status': 'error', 'message': 'ID is required for update'}, status=400)

            data = json.loads(request.body)
            try:
                project = Project.objects.get(id=id)
                for field in ['project_title', 'role', 'client', 'startdate', 'enddate', 'project_details']:
                    if field in data:
                        setattr(project, field, data[field])
                project.save()
                return JsonResponse({'status': 'success', 'message': 'Project updated successfully'}, status=200)
            except Project.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)

        elif request.method == 'DELETE':
            if not id:
                return JsonResponse({'status': 'error', 'message': 'ID is required for delete'}, status=400)

            try:
                project = Project.objects.get(id=id)
                project.delete()
                return JsonResponse({'status': 'success', 'message': 'Project deleted successfully'}, status=200)
            except Project.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)

        else:
            return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
def skills_view(request, id=None):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            user_id = data.get('user')

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

            skill = Skills.objects.create(
                user=user,
                name=data.get('skillname', '').strip()
            )
            return JsonResponse({'status': 'success', 'message': 'Skill saved successfully', 'id': skill.id}, status=201)

        elif request.method == 'GET':
            user_id = request.GET.get('user')
            if not user_id:
                return JsonResponse({'status': 'error', 'message': 'user is required'}, status=400)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

            if id:
                try:
                    skill = Skills.objects.get(id=id, user=user)
                    skill_data = {
                        'id': skill.id,
                        'name': skill.name,
                    }
                    return JsonResponse({'status': 'success', 'skill': skill_data}, status=200)
                except Skills.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Skill not found'}, status=404)
            else:
                skills = Skills.objects.filter(user=user)
                skill_list = list(skills.values('id', 'name'))
                return JsonResponse({'status': 'success', 'skills': skill_list}, status=200)

        elif request.method == 'PUT':
            if not id:
                return JsonResponse({'status': 'error', 'message': 'ID is required for update'}, status=400)

            data = json.loads(request.body)
            user_id = data.get('user')

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

            try:
                skill = Skills.objects.get(id=id, user=user)
                skill.name = data.get('skillname', skill.name).strip()
                skill.save()
                return JsonResponse({'status': 'success', 'message': 'Skill updated successfully'}, status=200)
            except Skills.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Skill not found'}, status=404)

        elif request.method == 'DELETE':
            if not id:
                return JsonResponse({'status': 'error', 'message': 'ID is required for delete'}, status=400)

            # Get user from query string since DELETE should not have body
            user_id = request.GET.get('user')
            if not user_id:
                return JsonResponse({'status': 'error', 'message': 'User ID is required'}, status=400)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

            try:
                skill = Skills.objects.get(id=id, user=user)
                skill.delete()
                return JsonResponse({'status': 'success', 'message': 'Skill deleted successfully'}, status=200)
            except Skills.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Skill not found'}, status=404)

        else:
            return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
@csrf_exempt
def AddEducation(request, id=None):
    try:
        user_id = request.GET.get('user_id')
        if request.method == "POST":
            data = json.loads(request.body)
            try:
                user = User.objects.get(id=data.get('user'))
                education = Education.objects.create(
                    user=user,
                    degree=data.get('degree'),
                    university=data.get('university'),
                    course_type=data.get('course_type'),
                    startdate=data.get('startdate'),
                    enddate=data.get('enddate'),
                    specialization=data.get('specialization'),
                    course_duration=data.get('course_duration'),
                    grading_system=data.get('grading_system'),
                    marks=data.get('marks'),
                )
                return JsonResponse({'status': 'success', 'message': 'Education created successfully', 'id': education.id}, status=201)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

        elif request.method == "GET":
            if not user_id:
                return JsonResponse({'status': 'error', 'message': 'Missing user_id'}, status=400)
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

            if id:
                try:
                    education = Education.objects.get(id=id, user=user)
                    education_data = {
                        'id': education.id,
                        'degree': education.degree,
                        'university': education.university,
                        'course_type': education.course_type,
                        'startdate': education.startdate,
                        'enddate': education.enddate,
                        'specialization': education.specialization,
                        'course_duration': education.course_duration,
                        'grading_system': education.grading_system,
                        'marks': education.marks,
                    }
                    return JsonResponse({'status': 'success', 'data': education_data}, status=200)
                except Education.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Education not found'}, status=404)
            else:
                educations = Education.objects.filter(user=user)
                if not educations.exists():
                    return JsonResponse({'status': 'success', 'data': []}, status=200)
                education_list = list(educations.values())
                return JsonResponse({'status': 'success', 'data': education_list}, status=200)

        elif request.method == "PUT":
            if not id:
                return JsonResponse({'status': 'error', 'message': 'ID is required for update'}, status=400)

            data = json.loads(request.body)
            try:
                education = Education.objects.get(id=id)
                for field in ['degree', 'university', 'course_type', 'startdate', 'enddate', 'specialization', 'course_duration', 'grading_system', 'marks']:
                    if field in data:
                        setattr(education, field, data[field])
                education.save()
                return JsonResponse({'status': 'success', 'message': 'Education updated successfully'}, status=200)
            except Education.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Education not found'}, status=404)

        elif request.method == "DELETE":
            if not id:
                return JsonResponse({'status': 'error', 'message': 'ID is required for delete'}, status=400)

            try:
                education = Education.objects.get(id=id)
                education.delete()
                return JsonResponse({'status': 'success', 'message': 'Education deleted successfully'}, status=200)
            except Education.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Education not found'}, status=404)

        else:
            return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def GetResumeData(request):
    if request.method == "GET":
        try:
            user = request.GET.get('user_id')
            basic = BasicDetails.objects.filter(user=user).first()
            experiences = Experience.objects.filter(user=user).values()
            educations = Education.objects.filter(user=user).values()
            projects = Project.objects.filter(user=user).values()
            skills = Skills.objects.filter(user=user).values('name')

            resume_data = {
                "basic": {
                    "name": basic.name if basic else "",
                    "email": basic.email if basic else "",
                    "phone": basic.phone if basic else "",
                    "summary": basic.summary if basic else "",
                    "linkedin": basic.linkedin if basic else "",
                    "github": basic.github if basic else "",
                    "website": basic.website if basic else "",
                },
                "experience": list(experiences),
                "education": list(educations),
                "projects": list(projects),
                "skills": [skill['name'] for skill in skills]
            }

            return JsonResponse({"status": "success", "data": resume_data}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Only GET is allowed"}, status=405)